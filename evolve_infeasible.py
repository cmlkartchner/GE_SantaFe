

from ge_utils import Gene
import random
from ge_utils import generate_phenotype, crossover
import time
GENE_LEN = 100
POPULATION_SIZE = 50
RULES = {
        "<code>": ["<code>", "<progs>", "<progs>"],
        "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
        "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
        "<prog2>" : ["prog2(<progs>,<progs>)"],
        "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
        "<op>" :["left","right","move"] 
    }

def generate_population(size, genome_length):
    genes = [Gene([random.randint(0, 100) for i in range(genome_length)]) for i in range(size)]
    for gene in genes: # generate phenotypes
        gene.phenotype = generate_phenotype(RULES, "<code>", gene)
    return genes

def fitness(gene: Gene):
    # the fitness of an infeasible is the number of nonterminals
    # percentage of terminals -> higher is better
    assert gene is not None
    pheno = gene.phenotype
    num_nonterminals = pheno.count("<")
    pheno = pheno.replace("<prog", "") # get rid of nonterminals that look like terminals

    num_terminals = 0
    for terminal in ["if_food_ahead", "left", "right", "move", "prog2", "prog3"]:
        num_terminals += pheno.count(terminal)

    return num_terminals/(num_nonterminals + num_terminals)

def sense(gene, population):
    # sampling from infeasible individuals
    gene.memory = random.sample(population, 5)

def act(gene: Gene):
    # add genotype
    # perform selection, crossover, mutation
    # evaluate fitness
    # highest wins
    gene.memory.append(gene)
    sorted_genes = sorted(gene.memory, key=lambda x: fitness(x))
    new_population = sorted_genes[:2] # keep the top 2 automatically

    j = 0
    while j < len(gene.memory)/2 - 1:
        parents = selection_pair(gene.memory, fitness)
        children = crossover(parents[0], parents[1])
        for child in children:
            child.mutate()
        new_population.extend(children)
        j += 1
    
    # eval new population and return the best
    for gene in new_population:
        gene.phenotype = generate_phenotype(RULES, "<code>", gene)
    new_population = sorted(new_population, key=lambda x: fitness(x))

    return new_population[0]
    

def update(original, new):
    if fitness(new) > fitness(original):
        return new
    return original

def selection_pair(population, fitness_func):
    population = population[:] # working with a copy just in case
    weights=[fitness(gene) for gene in population]

    if sum(weights) <= 0:
        return random.choices(population, k=2)

    return random.choices(population, weights=weights, k=2)

def evolve():
    population = generate_population(POPULATION_SIZE, GENE_LEN) # create population
    fitnesses = [fitness(gene) for gene in population]
    print(fitnesses)
    print("")
    solutions = [] # store feasible genes created

    for i in range(1000): # 1000 generations
        new_population = []
        for gene in population:
            # run the genes
            sense(gene, population) # each agent collects neighboring genes
            new_gene = act(gene) # each agent evolves their gene pool
            new_gene = update(gene, new_gene) # add new if better than currenct

            if fitness(gene) == 1:
                solutions.append(gene)
                new_population.append(generate_population(1, GENE_LEN)[0]) # refill
            else:  
                new_population.append(new_gene)
        population = new_population
    
    return solutions

results = evolve()
fitnesses = [fitness(gene) for gene in results]

for gene in results:
    print(gene.phenotype)
    print("_____________")

print(fitnesses)
