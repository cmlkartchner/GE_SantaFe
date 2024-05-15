from ge_utils import Gene
import random
from agent import agent, 


# this is master which should import basically all other files

# create the agents
def generate_population(size, genome_length):
    genes = [Gene([random.randint(0, 100) for i in range(genome_length)]) for i in range(size)]
    for gene in genes: # generate phenotypes
        gene.phenotype = generate_phenotype(RULES, "<code>", gene)
    return genes


# go through every agent, 