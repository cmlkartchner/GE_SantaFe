import random
from ge_utils import Gene, crossover
from agent import Agent
from constants import GENE_LEN, RULES
# starting position of each agent should be randomized
# use probability to figure out how many neighbors to sample

class EvolveManager:
    def __init__(self) -> None:
        self.population = []
    def generate_population(self, size, grid):
        self.population = [Agent(grid) for i in range(size)] # agent automatically generates initial genotype

    def sense(self, agent):
        # given an agent, set their memory variable to a sample of the population list
        # sample neighbors, take their genes
        num_neighbors = min(random.randint(1,10), len(self.population))
        neighbors = random.sample(self.population, num_neighbors)
        agent.gene.memory = [neighbor.gene for neighbor in neighbors]
        
    def act(self, gene: Gene, agent):
        # add genotype
        # perform selection, crossover, mutation
        # evaluate fitness
        # best genotype returned
        agent.memory.append(agent.gene) #add agent's own gene
        sorted_genes = sorted(agent.memory, key=lambda x: x.cost)
        new_genes = sorted_genes[:2] # keep the top 2 automatically

        j = 0
        while j < len(agent.memory)/2 - 1:
            parents = self.selection_pair(agent.memory)
            children = crossover(parents[0], parents[1])
            for child in children:
                child.mutate()
            new_genes.extend(children)
            j += 1
        
        # eval new population and return the best
        for gene in new_genes:
            gene.phenotype = gene.generate_phenotype(RULES, "<code>")
        new_genes = sorted(new_genes, key=lambda x: x.cost)
        return new_genes[0]
        
    def update(self, original_gene, new_gene):
        # given two genotypes, return the one with the higher cost
        if original_gene.cost < new_gene.cost:
            return new_gene
        return original_gene
    
    def selection_pair(self, genes):
        weights=[gene.cost for gene in genes]
        if sum(weights) <= 0:
            return random.choices(genes, k=2)
        return random.choices(genes, weights=weights, k=2)