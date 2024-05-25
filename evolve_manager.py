import random
from ge_utils import Gene, crossover
from agent import Agent
from constants import GENE_LEN, RULES
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
        while j < len(agent.memory)/2 - 1:
            parents = self.selection_pair(agent.memory)
            children = crossover(parents[0], parents[1])
            for child in children:
                child.mutate()
            new_genes.extend(children)
            j += 1
        
        #concern:our history dictionary will get too full...we need to reuse the same temp ids
        # create agents for each gene (necessary to evaluate gene)..best agent overrides current

        # clear history dictionay for temp ids
        for i in range(len(self.temp_ids)):
            agent.grid.history[self.temp_ids[0]] = set()

        temp_agents = []
        for i in range(len(new_genes)):
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