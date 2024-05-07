import re
import random
import numpy as np
from math import inf, log, sqrt, sin, cos

GENE_LEN = 10
NUM_GENERATIONS = 20

planets = {
    "Venus": (0.72, 0.61),
    "Earth": (1.00, 1.00),
    "Mars": (1.52, 1.84),
    "Jupiter": (5.20, 11.90),
    "Saturn": (9.53, 29.40),
    "Uranus": (19.10, 83.50)
}

rules = {
    "<expr>": ["<expr><op><expr>", 
                "<sub-expr>"],
    "<sub-expr>": ["<func>(<var>)",
                    "<var>",
                    "<var>**<n>"],
    "<func>": ["sin", "cos", "log", "sqrt"],
    "<op>": ["+", "-", "*"],
    "<var>": ["distance",
            "distance**<n>",
            "<n>"],
    "<n>": ["1", "2", "3", "4"]
}

class Gene():
    def __init__(self, genotype) -> None:
        self.genotype = genotype
        self.current_codon = 0
        self.phenotype = None
        self.cost = 0
    
    def get_codon(self):
        return self.genotype[self.current_codon]
    
    def mutate(self):
        i = 0
        while i < len(self.genotype):
            if np.random.random() > 0.8:
                self.genotype[i] = np.random.randint(0, 100)
            i += 1
    

def generate_string(rules, start_symbol, gene):
    # for each codon
    expression = start_symbol
    expression = parse_expression(rules, start_symbol, gene, expression)
    return expression

def parse_expression(rules, expression, gene, terminal_string):
    non_terminals = re.findall("<[^>]+>", expression)
    # for each non-terminal:
    for non_terminal in non_terminals:
            if gene.current_codon >= len(gene.genotype):
                return terminal_string
            # decide on production rule
            productions = rules.get(non_terminal)
            production = productions[gene.get_codon() % len(productions)]

            # substitute the non-terminal with the decided on production
            terminal_string = re.sub(non_terminal, production, terminal_string, 1)

            # ++current_codon
            gene.current_codon += 1
            
            # repeat on the non-terminals in the production
            terminal_string = parse_expression(rules, production, gene, terminal_string)
    return terminal_string
    
def evaluate_cost(expression):
    # for each planet
    results = []
    for planet in planets:
        distance = planets.get(planet)[0] # used by the expression (potentially)
        period = planets.get(planet)[1]
        try:
            result = eval(expression)
            results.append(log(1 + abs(period - result))) # FIXME: fix the math domain error
        except SyntaxError:
            # if invalid, give expression an infinite cost and return
            cost = inf
            return cost
    # calulate the mean of all the log(1 + (period - result))
    cost = np.mean(results)
    return cost

def crossover(gene_1, gene_2):
    # take the first half and combine with second half
    new_gene_1 = Gene(gene_1.genotype[:GENE_LEN//2])
    new_gene_1.genotype.extend(gene_2.genotype[GENE_LEN//2:])

    new_gene_2 = Gene(gene_2.genotype[:GENE_LEN//2])
    new_gene_2.genotype.extend(gene_1.genotype[GENE_LEN//2:])
    return new_gene_1, new_gene_2

### MAIN START ###
start_symbol = "<expr>"
current_generation = 0

# get starting generation
gene_1 = Gene(random.sample(range(1, 100), GENE_LEN))
gene_2 = Gene(random.sample(range(1, 100), GENE_LEN))

while current_generation < NUM_GENERATIONS:
    print(f"GENERATION {current_generation}")
    # parse
    gene_1.phenotype = generate_string(rules, start_symbol, gene_1)
    gene_2.phenotype = generate_string(rules, start_symbol, gene_2)

    # evaluate cost
    gene_1.cost = evaluate_cost(gene_1.phenotype)
    gene_2.cost = evaluate_cost(gene_2.phenotype)

    print(f"gene_1 cost: {gene_1.cost}")
    print(f"gene_2 cost: {gene_2.cost}\n")

    # set termination condition (specific to this problem; it means we have found Kepler's equation)
    if gene_1.cost == 0.021 or gene_2.cost == 0.021:
        break

    # crossover
    gene_1, gene_2 = crossover(gene_1, gene_2)

    # mutate
    gene_1.mutate()
    gene_2.mutate()

    current_generation += 1
