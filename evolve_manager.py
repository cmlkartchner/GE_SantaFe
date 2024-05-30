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
        #print(agent.id," has a cost of: ", agent.gene.cost)
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
        
        # create agents for each gene (necessary to evaluate gene)..best agent overrides current

        # clear history dictionay for temp ids
        for i in range(len(self.temp_ids)):
            agent.grid.history[self.temp_ids[0]] = set()

        temp_agents = []
        #tempagent.append.....is changing the codon and genotype of agent's gene
        for i in range(min(len(self.temp_ids), len(new_genes))): # len of new_genes varies and could be higher than temp_ids
            temp_agents.append(Agent(agent.grid, gene=new_genes[i], id=self.temp_ids[i]))
            temp_agents[i].run_phenotype(temp_agents[i].phenotype)

        temp_agents = sorted(temp_agents, key=lambda x: x.gene.cost, reverse=True)
        return temp_agents[0]
        
    def update(self, original_agent, new_agent):
        # given two genotypes, return the one with the higher cost
        
        if original_agent.gene.cost < new_agent.gene.cost:
            #print(original_agent.id, "of cost", original_agent.gene.cost, " will be replaced with a gene of cost: ", new_agent.gene.cost)
            # if we are going to return new agent, change its id, and transfer its prev history over to newid
            assert original_agent.grid == new_agent.grid
            grid = original_agent.grid

            new_id = random.randint(0, 1000000) # we must change id because the temp ids get their history cleared
            grid.history[new_id] = set(grid.history[new_agent.id]) # transfer history
            new_agent.id = new_id
            
            grid.history[original_agent.id] = set()
            return new_agent
        
        #print(original_agent.id, " will NOT be changed", original_agent.gene.cost, new_agent.gene.cost)
        return original_agent
    
    def selection_pair(self, genes):
        weights=[gene.cost for gene in genes]
        if sum(weights) <= 0:
            return random.choices(genes, k=2)
        return random.choices(genes, weights=weights, k=2)