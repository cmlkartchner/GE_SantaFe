import numpy as np
import re
import random
# from Grid_Food_EndExpect import Grid
from const import GENE_LEN

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
        newGeno = self.genotype.copy()
        for num in range(len(newGeno)):
            if num < (len(newGeno) * .2):
                if random.randint(1,10) > 6:
                    newGeno[num] = random.randint(-40, 40)
            elif num < (len(newGeno) * .6):
                if random.randint(1,10) > 5:
                    newGeno[num] = random.randint(-40, 40)
            elif num < (len(newGeno) * .8):
                if random.randint(1,10) > 4:
                    newGeno[num] = random.randint(-40, 40)
            else:
                if random.randint(1,10) > 2:
                    newGeno[num] = random.randint(-40, 40)
        return Gene(newGeno)
                
    # Performs a basic crossover between Genes
    def crossoverProduction(self, agents): 
        genotypes = []
        for agent in agents:
            genotypes.append(agent.gene.genotype)
        me = np.array(self.genotype)
        children = []
        for gene in genotypes:
            parent = np.array(gene)
            bottom = np.dot(parent, parent)
            if bottom == 0:
                children.append(Gene(np.round(me, decimals=0).astype(int).tolist()))
            else:
                scalar =  5 * (np.dot(me, parent) / bottom)
                child = scalar * parent
                children.append(Gene(np.round(child, decimals=0).astype(int).tolist()))
                children.append(Gene(np.ceil(child).astype(int).tolist()))
                children.append(Gene(np.floor(child).astype(int).tolist()))
        return children
        # nlength = len(genotypes)
        # initParents = np.array(genotypes)
        # parentMatrix = np.transpose(np.concatenate((initParents, np.zeros(((GENE_LEN - nlength), GENE_LEN)))))
        # child = np.transpose(np.matmul(parentMatrix, selfVector))
        # make list to interface with agent
        # children.append(Gene(child.astype(int).tolist()[0]))

if __name__ == "__main__":
    genes = []
    for i in range(4):
        genes.append(Gene([random.randint(0, 100) for x in range(GENE_LEN)]))
    gene = Gene([random.randint(0, 100) for x in range(GENE_LEN)])
    print(gene.crossoverProduction(genes))
    

# children = []
#         index = 1
#         splithold = genotypes[0][(GENE_LEN//2):]
#         while index < len(genotypes):            
#             new_gene_1 = genotypes[index][:(GENE_LEN//2)]
#             new_gene_1.extend(splithold)
#             splithold = genotypes[index][(GENE_LEN//2):]
#             genotypes[index] = new_gene_1.copy()
#             index += 1
#         new_gene = genotypes[0][:(GENE_LEN//2)]
#         new_gene.extend(splithold)
#         genotypes[0] = new_gene.copy()
#         for geno in genotypes:
#             children.append(Gene(geno))