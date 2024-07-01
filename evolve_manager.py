from math import inf
import random
from gene import Gene
from agent import Agent
from constants import GENE_LEN, RULES, NUM_COMPETITORS, SELECTION_PROPORTION, TOURNAMENT_SIZE, POP_SIZE, DIVERSITY_CONSTANT
import time

# ParetoSolution is exclusively for the NSGA-II functions included within EvolveManager
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
        self.initial_mutation_rate = 0.05
        self.generation_counter = 0
        self.total_generations = 100  # Set the total number of generations for adjusting mutation rate

    def generate_population(self, size, grid):
        self.population = [Agent(grid) for i in range(size)]  # agent automatically generates initial genotype
        self.temp_ids = [random.randint(0, 1000000) for i in range(size)]
        for agent in self.population:
            agent.gene.mutation_rate = self.initial_mutation_rate

    def sense(self, agent):
        agent.memory = random.sample(self.population, TOURNAMENT_SIZE)  # tournament_size to work with NSGA-II

    def total_crossover(self, parents, num_children):
        children = []
        for i in range(int(num_children / 2)):
            parent1 = random.randint(0, len(parents) - 1)
            parent2 = random.randint(0, len(parents) - 1)
            children.extend(Gene.crossover(parents[parent1], parents[parent2]))
        return children

    def check_references(objects):
        seen_addresses = set()
        for obj in objects:
            obj_address = id(obj)
            if obj_address in seen_addresses:
                return True  # Found a reference to the same object
            seen_addresses.add(obj_address)
        return False  # No references to the same object found

    def act(self, agent):
        if len(agent.memory) == 0:
            print("memory is empty")
            return agent
        agent.memory.append(agent)  # add agent's self

        sorted_genes = sorted(agent.memory, key=lambda x: x.novelty, reverse=True)
        new_genes = [gene.gene for gene in sorted_genes[:2]]  # get genes of the top two agents for next generation
        parents = self.novelty_selection(agent.memory)  # novelty selection

        parent_genes = [parent.gene.copy() for parent in parents]

        j = 0
        num_children = SELECTION_PROPORTION * len(self.population) - len(new_genes)  # number of children we still need to create
        while j < len(agent.memory) / 2 - 1:
            children = self.total_crossover(parent_genes, num_children)
            for child in children:
                child.mutate()
            new_genes.extend(children)
            j += 1

        for i in range(len(self.temp_ids)):
            agent.grid.history[self.temp_ids[0]] = set()

        temp_agents = []
        for i in range(min(len(self.temp_ids), len(new_genes))):
            temp_agents.append(Agent(agent.grid, gene=new_genes[i], id=self.temp_ids[i]))
            temp_agents[i].run_phenotype()

        for agent in temp_agents:
            agent.novelty = agent.novelty_score(population=temp_agents)

        temp_agents = sorted(temp_agents, key=lambda x: x.novelty, reverse=True)

        # Adjust mutation rate (example heuristic: decrease over generations)
        current_generation = self.calculate_current_generation()
        for temp_agent in temp_agents:
            new_rate = self.initial_mutation_rate * (1 - (current_generation / self.total_generations))
            temp_agent.gene.adjust_mutation_rate(new_rate)

        # Increment the generation counter
        self.generation_counter += 1

        return temp_agents[0]

    def calculate_current_generation(self):
        # Return the current generation counter
        return self.generation_counter

    def update(self, original_agent, new_agent):
        if original_agent.novelty < new_agent.novelty:
            assert original_agent.grid == new_agent.grid
            grid = original_agent.grid

            new_id = random.randint(0, 1000000)
            grid.history[new_id] = set(grid.history[new_agent.id])
            new_agent.id = new_id

            grid.history[original_agent.id] = set()
            return new_agent
        return original_agent

    def selection_pair(self, agents):
        weights = [agent.gene.cost for agent in agents]
        if sum(weights) <= 0:
            return random.choices(agents, k=2)
        return random.choices(agents, weights=weights, k=2)

    def tournament_selection(self, agents):
        parents = []
        weights = [agent.gene.cost for agent in agents]
        for i in range(NUM_COMPETITORS):
            if sum(weights) <= 0:
                competitors = random.choices(agents, k=2)
            else:
                competitors = random.choices(agents, weights=weights, k=NUM_COMPETITORS)
            parents.append(max(competitors, key=lambda x: x.gene.cost))
        return parents

    def novelty_selection(self, agents):
        weights = [agent.novelty for agent in agents]
        if sum(weights) <= 0:
            return random.choices(agents, k=NUM_COMPETITORS)  # random chance
        return random.choices(agents, weights=weights, k=NUM_COMPETITORS)  # weighted chance

    def nsga2_select(self, agents):
        sorted_fronts, solution_lookup = self.nondomination_sort(agents)
        self.calculate_crowding_dist(agents, solution_lookup)

        winners = []
        for i in range(POP_SIZE):
            participants = random.sample(agents, TOURNAMENT_SIZE)
            winners.append(self.pareto_tournament(participants, solution_lookup))
        return winners

    def nondomination_sort(self, agents):
        solutions = []
        solution_lookup = dict()
        for agent in agents:
            solution = ParetoSolution(agent)
            solutions.append(solution)
            solution_lookup.update({agent.id: solution})

        fronts = []
        first_front = []
        for solution_i in solutions:
            rank = 1
            food_eaten = solution_i.agent.food_touched
            moves_taken = solution_i.agent.distance
            for solution_j in solutions:
                if solution_i is solution_j:
                    continue
                if food_eaten > solution_j.agent.food_touched and moves_taken < solution_j.agent.distance:
                    solution_i.dominated_solutions.add(solution_j)
                elif food_eaten < solution_j.agent.food_touched and moves_taken > solution_j.agent.distance:
                    solution_i.domination_count += 1
            if solution_i.domination_count == 0:
                solution_i.rank = rank
                first_front.append(solution_i)

        front_rank = 1
        fronts.append(first_front)
        current_front = first_front
        while len(current_front) > 0:
            next_front = []
            for solution in current_front:
                for dominated_solution in solution.dominated_solutions:
                    dominated_solution.domination_count -= 1
                    if dominated_solution.domination_count == 0:
                        dominated_solution.rank = front_rank + 1
                        next_front.append(dominated_solution)
            front_rank += 1
            fronts.append(next_front)
            current_front = next_front

            return fronts, solution_lookup

    def calculate_crowding_dist(self, agents, solution_lookup: dict):
        food_eaten_sorted = sorted(agents, key=lambda x: x.food_touched, reverse=False)
        moves_taken_sorted = sorted(agents, key=lambda x: x.distance, reverse=False)
        agent_most_food = food_eaten_sorted[0]
        agent_least_food = food_eaten_sorted[-1]
        agent_most_moves = moves_taken_sorted[0]
        agent_least_moves = moves_taken_sorted[-1]

        solution_lookup.get(agent_most_food.id).crowding_dist = inf
        solution_lookup.get(agent_least_food.id).crowding_dist = inf
        solution_lookup.get(agent_most_moves.id).crowding_dist = inf
        solution_lookup.get(agent_least_moves.id).crowding_dist = inf

        max_dist = 0
        min_dist = inf
        for agent in agents:
            if agent is agent_most_food or agent is agent_least_food or agent is agent_most_moves or agent is agent_least_moves:
                continue
            agent_food_index = food_eaten_sorted.index(agent)
            neighbor1 = food_eaten_sorted[agent_food_index - 1]
            neighbor2 = food_eaten_sorted[agent_food_index + 1]
            food_dist = neighbor1.food_touched - neighbor2.food_touched

            agent_moves_index = moves_taken_sorted.index(agent)
            neighbor1 = moves_taken_sorted[agent_moves_index - 1]
            neighbor2 = moves_taken_sorted[agent_moves_index + 1]
            moves_dist = neighbor2.distance - neighbor1.distance

            dist = food_dist + moves_dist
            solution_lookup.get(agent.id).crowding_dist = dist
            if dist > max_dist:
                max_dist = dist
            elif dist < min_dist:
                min_dist = dist

        norm_factor = max_dist - min_dist
        if norm_factor == 0:
            for solution in solution_lookup.values():
                solution.crowding_dist = 0
        else:
            for solution in solution_lookup.values():
                solution.crowding_dist = (solution.crowding_dist - min_dist) / norm_factor

    def pareto_tournament(self, agents, solution_lookup):
        winning_agent = agents[0]
        winning_agent_solution = solution_lookup.get(winning_agent.id)
        for agent in agents:
            if agent is winning_agent:
                continue
            agent_solution = solution_lookup.get(agent.id)
            if agent_solution.rank < winning_agent_solution.rank:
                winning_agent = agent
                winning_agent_solution = agent_solution
            elif agent_solution.rank == winning_agent_solution.rank:
                if agent_solution.crowding_dist < winning_agent_solution.crowding_dist:
                    winning_agent = agent
                    winning_agent_solution = agent_solution
        return winning_agent
