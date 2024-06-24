from math import inf
import random
from gene import Gene
from agent import Agent
from constants import GENE_LEN, RULES, NUM_COMPETITORS, SELECTION_PROPORTION, TOURNAMENT_SIZE, POP_SIZE, DIVERSITY_CONSTANT
import time

# ParetoSolution is exclusively for the NSGA-II functions included within EvolveManager
# (A possible option for the act function)
class ParetoSolution:
    def __init__(self, agent) -> None:
        self.agent = agent
        self.domination_count = 0
        self.dominated_solutions = set()
        self.rank = 0
        self.crowding_dist = 0

# EvolveManager is the place for all the evolution functions used in evolve.py
class EvolveManager:
    def __init__(self) -> None:
        self.population = []
        
    def generate_population(self, size, grid):
        self.population = [Agent(grid) for i in range(size)] # agent automatically generates initial genotype
        self.temp_ids = [random.randint(0, 1000000) for i in range(size)]

    def sense(self, agent):
        # given an agent, set their memory variable to a sample of the population list
        agent.memory = random.sample(self.population, TOURNAMENT_SIZE) # tournament_size to work with NSGA-II
    
    def total_crossover(self, parents, num_children):
        # do however many random crossovers are needed to get num_children children
        children = []
        for i in range(int(num_children/2)):
            parent1 = random.randint(0, len(parents)-1)
            parent2 = random.randint(0, len(parents)-1)
            children.extend(Gene.crossover(parents[parent1], parents[parent2]))
        return children

    def check_references(objects): # random helper function to make sure no shared references
        seen_addresses = set()
        for obj in objects:
            obj_address = id(obj)
            if obj_address in seen_addresses:
                return True  # Found a reference to the same object
            seen_addresses.add(obj_address)
        return False  # No references to the same object found

    def act(self, agent):
        # add genotype (the agent, which contains the genotype) to the memory list
        # perform selection, crossover, mutation
        # evaluate fitness
        # best agent (with their genotype) returned
        if len(agent.memory) == 0:
            print("memory is empty")
            return agent
        agent.memory.append(agent) #add agent's self

        sorted_genes = sorted(agent.memory, key=lambda x: x.novelty, reverse=True)
        new_genes = [gene.gene for gene in sorted_genes[:2]] # get genes of the top two agents for next generation
        parents = self.novelty_selection(agent.memory) # novelty selection
        #parents = self.tournament_selection(agent.memory) # tournament selection
        #parents = self.nsga2_select(agent.memory) # NSGA-II selection to pick parents to create new_genes

        # turn parent agents to genes for crossover and mutation, also copy objects to AVOID shared references
        parent_genes = [parent.gene.copy() for parent in parents]

        j = 0
        num_children = SELECTION_PROPORTION * len(self.population) - len(new_genes) # number of children we still need to create
        while j < len(agent.memory)/2 - 1: # technically with the use of total_crossover the while loop should run 1 time
            children = self.total_crossover(parent_genes, num_children) 
            for child in children:
                child.mutate()
            new_genes.extend(children)
            j += 1
        # create agents for each gene (necessary to evaluate gene)..best agent overrides current

        # clear history dictionay for temp ids
        for i in range(len(self.temp_ids)):
            agent.grid.history[self.temp_ids[0]] = set()

        temp_agents = []
        for i in range(min(len(self.temp_ids), len(new_genes))): # len of new_genes varies and could be higher than temp_ids
            temp_agents.append(Agent(agent.grid, gene=new_genes[i], id=self.temp_ids[i]))
            temp_agents[i].run_phenotype()

        # use num_food array from all agents to calculate novelty
        for agent in temp_agents:
            agent.novelty = agent.novelty_score(population=temp_agents) # set novelty score
        # compare diversity of the population (diversity metric of fitness function)c
        #Agent.apply_diversity(temp_agents)
        # for agent in temp_agents:
        #     diff = agent.average_difference(temp_agents)/DIVERSITY_CONSTANT
        #     agent.gene.cost += diff

        temp_agents = sorted(temp_agents, key=lambda x: x.novelty, reverse=True)
        return temp_agents[0]
        
    def update(self, original_agent, new_agent):
        # given two genotypes, return the one with the higher cost
        if original_agent.novelty < new_agent.novelty:
            # if we are going to return new agent, change its id, and transfer its prev history over to newid
            assert original_agent.grid == new_agent.grid
            grid = original_agent.grid

            new_id = random.randint(0, 1000000) # we must change id because the temp ids get their history cleared
            grid.history[new_id] = set(grid.history[new_agent.id]) # transfer history
            new_agent.id = new_id
            
            grid.history[original_agent.id] = set()
            return new_agent
        return original_agent
    
    def selection_pair(self, agents):
        # select two agents at random, with probability proportional to their cost
        weights=[agent.gene.cost for agent in agents]
        if sum(weights) <= 0:
            return random.choices(agents, k=2)
        return random.choices(agents, weights=weights, k=2)

    def tournament_selection(self, agents): 
        # returns the list of winners
        # sample k competitors, return the one with the highest cost
        parents = []
        weights=[agent.gene.cost for agent in agents]
        for i in range(NUM_COMPETITORS):
            if sum(weights) <= 0:
                competitors = random.choices(agents, k=2)
            else:
                competitors = random.choices(agents, weights=weights, k=NUM_COMPETITORS) 
            parents.append(max(competitors, key=lambda x: x.gene.cost))
        return parents
    
    def novelty_selection(self, agents):
        # selection based on novelty (NOT FITNESS)
        weights=[agent.novelty for agent in agents]
        if sum(weights) <= 0:
            return random.choices(agents, k=NUM_COMPETITORS) # random chance
        return random.choices(agents, weights=weights, k=NUM_COMPETITORS) # weighted chance

    ###########################################
    # code for NSGA-II
    def nsga2_select(self, agents):
        # Non-dominated sorting: sort into ranks based on who dominates who
        sorted_fronts, solution_lookup = self.nondomination_sort(agents)

        # Calculate crowding distance (account for diversity in the population)
        self.calculate_crowding_dist(agents, solution_lookup)

        # Select population to go into a pareto tournament, higher rank will be more likely to win
        # but greater crowding distance is favored within each rank (i.e. a tie-breaker)
        winners = []
        for i in range(POP_SIZE):
            participants = random.sample(agents, TOURNAMENT_SIZE)
            winners.append(self.pareto_tournament(participants, solution_lookup))
        return winners

    def nondomination_sort(self, agents):
        # initialize list of solutions (solution = ParetoSolution object, basically an agent with some extra attributes)
        solutions = []
        solution_lookup = dict() # key: agent.id, value: ParetoSolution object
        for agent in agents:
            solution = ParetoSolution(agent)
            solutions.append(solution)
            solution_lookup.update({agent.id: solution})

        fronts = []
        first_front = []
        # rank the solutions
        for solution_i in solutions:
            rank = 1
            food_eaten = solution_i.agent.food_touched
            moves_taken = solution_i.agent.distance
            for solution_j in solutions:
                if solution_i is solution_j:
                    continue
                # if current_solution dominates agent.solution:
                if food_eaten > solution_j.agent.food_touched and moves_taken < solution_j.agent.distance:
                    solution_i.dominated_solutions.add(solution_j)
                # else if agent.solution dominates current_solution:
                elif food_eaten < solution_j.agent.food_touched and moves_taken > solution_j.agent.distance:
                    solution_i.domination_count += 1
            # if solution is not dominated by any other solution
            if solution_i.domination_count == 0:
                # add current_solution to first front
                solution_i.rank = rank
                first_front.append(solution_i)

        # initialize front index to first front
        front_rank = 1
        fronts.append(first_front)
        current_front = first_front
        # populate the rest of the fronts
        while len(current_front) > 0:
            # initialize list for the next front
            next_front = []
            for solution in current_front:
                # for each solution_j that is dominated by solution_i:
                for dominated_solution in solution.dominated_solutions:
                    dominated_solution.domination_count -= 1 # remove {current_front} front from consideration
                    if dominated_solution.domination_count == 0: # if solution_j only dominated by solution_i then it will be in the next front
                        dominated_solution.rank = front_rank + 1
                        next_front.append(dominated_solution)
            # get next front
            front_rank += 1
            fronts.append(next_front)
            current_front = next_front

            # return the list of fronts
            return fronts, solution_lookup

    def calculate_crowding_dist(self, agents, solution_lookup: dict):
        # find the best performing and worst performing solution for each objective (sort the individuals again based on food eaten and moves taken)
        food_eaten_sorted = sorted(agents, key=lambda x: x.food_touched, reverse=False)
        moves_taken_sorted = sorted(agents, key=lambda x: x.distance, reverse=False)
        agent_most_food = food_eaten_sorted[0]
        agent_least_food = food_eaten_sorted[-1]
        agent_most_moves = moves_taken_sorted[0] # the worst in moves
        agent_least_moves = moves_taken_sorted[-1] # the best in moves

        # set boundary agents to infinite distance
        solution_lookup.get(agent_most_food.id).crowding_dist = inf
        solution_lookup.get(agent_least_food.id).crowding_dist = inf
        solution_lookup.get(agent_most_moves.id).crowding_dist = inf
        solution_lookup.get(agent_least_moves.id).crowding_dist = inf

        max_dist = 0
        min_dist = inf
        for agent in agents:
            if agent is agent_most_food or agent is agent_least_food or agent is agent_most_moves or agent is agent_least_moves:
                continue
            # calculate normalized distance between food eaten and two nearest neighbors
            agent_food_index = food_eaten_sorted.index(agent)
            neighbor1 = food_eaten_sorted[agent_food_index - 1] # ate more
            neighbor2 = food_eaten_sorted[agent_food_index + 1] # ate less
            food_dist = neighbor1.food_touched - neighbor2.food_touched

            # calculated normalized distance between moves taken and two nearest neighbors
            agent_moves_index = moves_taken_sorted.index(agent)
            neighbor1 = moves_taken_sorted[agent_moves_index - 1] # moved less
            neighbor2 = moves_taken_sorted[agent_moves_index + 1] # moved more
            moves_dist = neighbor2.distance - neighbor1.distance

            #print("food_dist", food_dist, "moves_dist", moves_dist, "sum", food_dist + moves_dist)

            # sum the distances
            dist = food_dist + moves_dist
            solution_lookup.get(agent.id).crowding_dist = dist
            if dist > max_dist:
                max_dist = dist
            elif dist < min_dist:
                min_dist = dist
        
        # normalize the crowding distances if max_dist != min_dist
        norm_factor = max_dist - min_dist
        if norm_factor == 0: # handle 0 case (no diversity in the population)
            for solution in solution_lookup.values():
                solution.crowding_dist = 0  # TODO: does it matter what the default value is?
        else:
            for solution in solution_lookup.values():
                solution.crowding_dist = (solution.crowding_dist - min_dist) / norm_factor

    def pareto_tournament(self, agents, solution_lookup):
        # given a population of agents:
        winning_agent = agents[0]
        winning_agent_solution = solution_lookup.get(winning_agent.id)
        for agent in agents:
            # if rank is higher than current winning agent, choose that one
            if agent is winning_agent:
                continue
            agent_solution = solution_lookup.get(agent.id)
            if agent_solution.rank < winning_agent_solution.rank:
                winning_agent = agent
                winning_agent_solution = agent_solution
            # else if rank is same as current winning agent
            elif agent_solution.rank == winning_agent_solution.rank:
                # if crowding distance is smaller than the distance of the current winning agent, choose that one
                if agent_solution.crowding_dist < winning_agent_solution.crowding_dist:
                    winning_agent = agent
                    winning_agent_solution = agent_solution
        return winning_agent

