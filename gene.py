import numpy as np
import re
import random
from GGraph_Node import GGraph
from const import GENE_LEN, RULES

class Gene():
    def __init__(self, genotype) -> None:
        self.genotype = genotype
        self.current_codon = 0
        self.cost = 0
        self.index = 0
    
    def get_codon(self):
        return self.genotype[self.current_codon]
    
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
    
    def mutate(self):
        for num in self.genotype:
            if np.random.random() > 0.8:
                num = random.randint(0, 100)   # noqa: F841
                
    # Performs a basic crossover between Genes
    def crossoverProduction(self, agents): 
        genotypes = []
        for agent in agents:
            genotypes.append(agent.gene.genotype)
        genotypes.append(self.genotype)
        children = []
        index = 0
        while index < len(genotypes) - 1:            
            new_gene_1 = genotypes[index][:(GENE_LEN//2)]
            new_gene_1.extend(genotypes[index + 1][:(GENE_LEN//2)])
            new_gene_2 = genotypes[index][(GENE_LEN//2):]
            new_gene_2.extend(genotypes[index + 1][(GENE_LEN//2):])
            genotypes[index] = new_gene_1.copy()
            genotypes[index + 1] = new_gene_2.copy()
            index += 1
        for geno in genotypes:
            children.append(Gene(geno))
        return children

if __name__ == "__main__":
    gene = Gene(np.random.randint(101, size=GENE_LEN))
    print(gene.generate_phenotype(GGraph(RULES), '<code>'))