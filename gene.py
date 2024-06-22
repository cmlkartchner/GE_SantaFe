import numpy as np
import re
import random
from GGraph_Node import GGraph
from const import GENE_LEN, RULES

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
        for non_terminal in non_terminals:
                if gene.current_codon >= len(gene.genotype):
                    return terminal_string
                
                production = rules.find_by_mod(non_terminal, gene.get_codon())

                # substitute the non-terminal with the decided on production
                terminal_string = re.sub(non_terminal, production, terminal_string, 1)

                gene.current_codon += 1
                
                # repeat on the non-terminals in the production
                terminal_string = Gene.parse_expression(rules, production, gene, terminal_string)
        return terminal_string
                
    def finish_expression(rules, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", terminal_string)
        for non_terminal in non_terminals:
                if gene.current_codon >= len(gene.genotype):
                    gene.current_codon = 0
                    
                production = rules.find_by_weight(non_terminal, gene.get_codon())

                # substitute the non-terminal with the decided on production
                terminal_string = re.sub(non_terminal, production, terminal_string, 1)

                gene.current_codon += 1
        return terminal_string
    
    # Generates the program/expression represented by the gene i.e. the phenotype.
    def generate_phenotype(self, rules, start_symbol):
        expression = Gene.parse_expression(rules, start_symbol, self, start_symbol)
        self.current_codon = 0
        expression = Gene.finish_expression(rules, self, expression)
        return expression
        # OLD
        # while True:
        #     expression = Gene.parse_expression(rules, expression, self, expression)
        #     # ensure that is contains A function
        #     if "<" not in expression and ">" not in expression and "(" in expression:
        #         break
        #     # my issue
        #     num += 1
        #     print(f'AGAINBRO{num} \n{expression}')
        #     self.current_codon = 0
    
    # Performs a basic crossover between two Genes
    def crossover(gene_1, gene_2): 
        # take the first half and combine with second half
        new_gene_1 = Gene(gene_1.genotype[:GENE_LEN//2])
        new_gene_1.genotype.extend(gene_2.genotype[GENE_LEN//2:])

        new_gene_2 = Gene(gene_2.genotype[:GENE_LEN//2])
        new_gene_2.genotype.extend(gene_1.genotype[GENE_LEN//2:])
        return new_gene_1, new_gene_2

if __name__ == "__main__":
    gene = Gene(np.random.randint(101, size=GENE_LEN))
    print(gene.generate_phenotype(GGraph(RULES), '<code>'))


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