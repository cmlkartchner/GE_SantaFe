import random
from ge_utils import Gene, crossover
from agent import Agent
from constants import GENE_LEN, RULES, NUM_COMPETITORS, SELECTION_PROPORTION
import time
# starting position of each agent should be randomized
# use probability to figure out how many neighbors to sample
class EvolveManager:
    def __init__(self) -> None:
        self.population = []
        
    def generate_population(self, size, grid):
        self.population = [Agent(grid) for i in range(size)] # agent automatically generates initial genotype
        self.temp_ids = [random.randint(0, 1000000) for i in range(size)]

    def sense(self, agent):
        # given an agent, set their memory variable to a sample of the population list
        # sample neighbors, take their genes
        num_neighbors = min(random.randint(1,10), len(self.population))
        neighbors = random.sample(self.population, num_neighbors)
        agent.memory = [neighbor.gene for neighbor in neighbors]
    
    def total_crossover(self, parents, num_children):
        # do x number of crossover using the parents 
        children = []
        for i in range(int(num_children/2)):
            parent1 = random.randint(0, len(parents)-1)
            parent2 = random.randint(0, len(parents)-1)
            children.extend(crossover(parents[parent1], parents[parent2]))
        return children

    def act(self, agent):
        # add genotype
        # perform selection, crossover, mutation
        # evaluate fitness
        # best agent (with their genotype) returned
        if len(agent.memory) == 0:
            return agent.gene
        agent.memory.append(agent.gene) #add agent's own gene
        sorted_genes = sorted(agent.memory, key=lambda x: x.cost, reverse=True)
        new_genes = sorted_genes[:2] # keep the top 2 automatically
        j = 0

        parents = self.tournament_selection(agent.memory) # tournament selection
        while j < len(agent.memory)/2 - 1:
            num_children = SELECTION_PROPORTION * len(agent.memory) - len(new_genes)
            children = self.total_crossover(parents, num_children) 
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
            temp_agents[i].run_phenotype(temp_agents[i].phenotype)

        temp_agents = sorted(temp_agents, key=lambda x: x.gene.cost, reverse=True)
        return temp_agents[0]
        
    def update(self, original_agent, new_agent):
        # given two genotypes, return the one with the higher cost
        
        if original_agent.gene.cost < new_agent.gene.cost:
            # if we are going to return new agent, change its id, and transfer its prev history over to newid
            assert original_agent.grid == new_agent.grid
            grid = original_agent.grid

            new_id = random.randint(0, 1000000) # we must change id because the temp ids get their history cleared
            grid.history[new_id] = set(grid.history[new_agent.id]) # transfer history
            new_agent.id = new_id
            
            grid.history[original_agent.id] = set()
            return new_agent
        return original_agent
    
    def selection_pair(self, genes):
        weights=[gene.cost for gene in genes]
        if sum(weights) <= 0:
            return random.choices(genes, k=2)
        return random.choices(genes, weights=weights, k=2)
    

    def tournament_selection(self, genes): 
        # returns the list of winners
        # sample k competitors, return the one with the highest cost
        parents = []
        weights=[gene.cost for gene in genes]
        for i in range(NUM_COMPETITORS):
            if sum(weights) <= 0:
                competitors = random.choices(genes, k=2)
            else:
                competitors = random.choices(genes, weights=weights, k=NUM_COMPETITORS) 
            parents.append(max(competitors, key=lambda x: x.cost))
        return parents[:]

        
        