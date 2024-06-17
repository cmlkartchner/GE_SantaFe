import numpy as np
import re
import random
from const import GENE_LEN

class Gene():
    def __init__(self, genotype) -> None:
        self.genotype = genotype
        self.current_codon = 0
        self.phenotype = None
        self.cost = 0
        self.index = 0
    
    def get_codon(self):
        return self.genotype[self.current_codon]
    
    def mutate(self):
        i = 0
        while i < len(self.genotype):
            if np.random.random() > 0.8:
                self.genotype[i] = random.randint(0, 100)
            i += 1

# A recursive function that evaluates non-terminals in a string in a depth-first search.
    def parse_expression(rules, expression, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", expression)
        # for each non-terminal:
        for non_terminal in non_terminals:
                # needs a better limiter
                if gene.current_codon >= len(gene.genotype):
                    return terminal_string
                # decide on production rule
                productions = rules.get(non_terminal) # list of possible productions
                production = productions[gene.get_codon() % len(productions)] # select one

                # substitute the non-terminal with the decided on production
                terminal_string = re.sub(non_terminal, production, terminal_string, 1)

                # ++current_codon
                gene.current_codon += 1
                
                # repeat on the non-terminals in the production
                terminal_string = Gene.parse_expression(rules, production, gene, terminal_string)
        return terminal_string
    
# Generates the program/expression represented by the gene i.e. the phenotype.
    def generate_phenotype(self, rules, start_symbol):
        num = 0
        expression = Gene.parse_expression(rules, start_symbol, self, start_symbol)
        while True:
            expression = Gene.parse_expression(rules, expression, self, expression)
            # ensure that is contains A function
            if "<" not in expression and ">" not in expression and "(" in expression:
                break
            # my issue
            num += 1
            print(f'AGAINBRO{num} \n{expression}')
            self.current_codon = 0
        return expression
    
# Performs a basic crossover between two Genes
    def crossover(gene_1, gene_2): 
        # take the first half and combine with second half
        new_gene_1 = Gene(gene_1.genotype[:GENE_LEN//2])
        new_gene_1.genotype.extend(gene_2.genotype[GENE_LEN//2:])

        new_gene_2 = Gene(gene_2.genotype[:GENE_LEN//2])
        new_gene_2.genotype.extend(gene_1.genotype[GENE_LEN//2:])
        return new_gene_1, new_gene_2


# """
# Fitness evaluation function;
# Change the try block based on however you want to calculate fitness
# """    
# def evaluate_fitness(expression):
#     try:
#         result = eval(expression) # TODO: change to exec() for actual programs
#         cost = result
#     except SyntaxError:
#         # if invalid string (i.e. there are still non-terminals), give expression an infinite cost and return
#         cost = inf
#         return cost
#     return cost