import numpy as np
import re
from math import inf
import random
from constants import GENE_LEN, MUTATION_PROBABILITY
import time

class Gene():
    def __init__(self, genotype, cost=0, mutation_rate = MUTATION_PROBABILITY) -> None:
        self.genotype = genotype[:] # list of integers used to generate the phenotype
        self.current_codon = 0 # the index of self.genotype being read (updated in parse_expression)
        self.phenotype = None # string representation of the program generated using the grammar
        self.cost = cost # the fitness of self.genotype
        self.mutation_rate = mutation_rate # the probability of a mutation
    def copy(self):
        return Gene(self.genotype[:], self.cost)
    def get_codon(self):
        return self.genotype[self.current_codon]
    
    def mutate(self):
        i = 0
        while i < len(self.genotype):
            if np.random.random() < self.mutation_rate:  # use the mutation rate
                self.genotype[i] = np.random.randint(0, 100)
            i += 1

    def adjust_mutation_rate(self, generation):
    # Increase mutation rate if no significant improvement
        if generation > 10 and self.no_improvement_for > 5:
            self.mutation_rate = min(0.1, self.mutation_rate * 1.5)
        else:
            self.mutation_rate = max(0.01, self.mutation_rate * 0.9)

    """
    Generates the program/expression represented by the gene i.e. the phenotype.
    rules: a dictionary containing production rules with key value pairs (string: string[]) where
            the key is in format "<val>"
    start_symbol: a string whose value isthe symbol you begin parsing from;
            must be a symbol within rules
    gene: a Gene whose current_codon is 0
    """
    def generate_phenotype(self, rules, start_symbol):
        while True:
            expression = start_symbol
            expression = Gene.parse_expression(rules, start_symbol, self, expression)
            if "<" not in expression and ">" not in expression and "(" in expression: # ensure that is contains A function
                break
            self.genotype = [random.randint(0,100) for i in range(GENE_LEN)] # try again
            self.current_codon = 0
        return expression
 

    """
    A recursive function that evaluates non-terminals in a string in a
    depth-first search.
    rules: a dictionary containing the production rules;
            same format as the rules in generate_phenotype
    expression: a string of symbols to evaluate;
            corresponds with the production taken
    gene: the Gene with the genotype to evaluate
    terminal_string: the string containing the current state of the entire parse;
            NOTE - if the parser reaches the end of the genotype, the terminal string
                    has a chance of still containing non-terminals
    """
    def parse_expression(rules, expression, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", expression)
        # for each non-terminal:
        for non_terminal in non_terminals:
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

    """
    Performs a basic crossover between two Genes;
    Modify to do the crossover strategy you want
    """
    def crossover(gene_1, gene_2):
        # take the first half and combine with second half
        new_gene_1 = Gene(gene_1.genotype[:GENE_LEN//2])
        new_gene_1.genotype.extend(gene_2.genotype[GENE_LEN//2:])

        new_gene_2 = Gene(gene_2.genotype[:GENE_LEN//2])
        new_gene_2.genotype.extend(gene_1.genotype[GENE_LEN//2:])
        return new_gene_1, new_gene_2

    def __str__(self) -> str:
        if self.phenotype is None:
            return "No phenotype"
        return self.phenotype


if __name__ == "__main__":
    # test the functions
    rules = {
        "<code>": ["<code>", "<progs>", "<progs>"],
        "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
        "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
        "<prog2>" : ["prog2(<progs>,<progs>)"],
        "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
        "<op>" :["left","right","move"] 
    }

    gene = Gene([random.randint(0,9) for i in range(GENE_LEN)])
    expression = gene.generate_phenotype(rules, "<code>")