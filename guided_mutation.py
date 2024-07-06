
from tree import Node
import random
from constants import GENE_LEN
import re
from gene import Gene
import time
RULES = { # each item in nested list will be a child to add to parent
      "S":[["E", "=", "N"]],
      "E":[["E", "+", "E"],["E", "-", "E"],["E", "+", "F"], ["F", "-", "E"], ["N"]],
      "F":[["N"]],
      "N":[["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]]
    }
non_terminals_list = ["S", "E", "F", "N"]
terminals = ["+", "-", "=", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

master_node = Node("<S>", [])

def parse_expression(rules, gene, tree, non_terminals):
        # non_termianls = list of references to leaf non-termianls in tree not finished (TREES)
        # for each non-terminal:
        for non_terminal in non_terminals:
                symbol = non_terminal.symbol
                if gene.current_codon >= len(gene.genotype):
                    return tree
                # decide on production rule
                productions = rules.get(symbol) # list of possible productions
                
                production = productions[gene.get_codon() % len(productions)] # select one

                # the production needs to be used to append to the tree
                insert_point = -len(non_terminals)
                for child in production: #[E, +, E] # "E" is a child
                    new_node = Node(child, [])
                    non_terminal.add_child(new_node) # expand tree

                    # update non-terminal list
                    if child in non_terminals_list:
                        non_terminals.insert(insert_point, new_node) # add left to right, but before existing elements
                non_terminals.remove(non_terminal)

                # ++current_codon
                gene.current_codon += 1
                
                #print(tree)
                print(gene.current_codon, len(gene.genotype))
                time.sleep(.2)
                # repeat on the non-terminals in the production
                parse_expression(rules, gene, tree, non_terminals)


# STEP 1: Produce a tree from the grammar


def generate_phenotype(self, rules, start_symbol):
        while True:
            expression = start_symbol
            expression = Gene.parse_expression(rules, start_symbol, self, expression)
            if "<" not in expression and ">" not in expression and "(" in expression: # ensure that is contains A function
                print("ALL GOOD")
                break
            print("bad need to run again")
            self.genotype = [random.randint(0,100) for i in range(GENE_LEN)] # try again
            self.current_codon = 0
        return expression

g = Gene([0,0,4,0,4,3,9], 0) #[random.randint(0,100) for i in range(100)]
starting_tree = Node("S", [])
parse_expression(RULES, g, starting_tree, [starting_tree])
print(starting_tree)
# CN1 = mutating node
# create tree to show the whole grammar translation process

#1: mark each non-terminal (except root) with tuple (non-terminal, coord)

#2: If there are terminals, select 1 at random to be CN1. Else you
# can only cross at the root and the result is same as parents

#3: R = [list of productions of the parent of CN1]

# A means the parent symbol of CN1
#4: calculate T = (l,p,a)
# a = the derivation that the parent A does
# p = position of the crossover node in the this derivation
    #ex: E+E -> crossover E is position 1
# l = num non-terminal & terminals in the derivation

#5: Remove from R the productions with a different l

#6: Remove from R productions with a different non-terminal

#7: X = [the symbols in R that are in position p]

#8: If X not empty, select 1 at random to be CS
    #PN = all nodes of second parent that contain CS
# Else, return to step 2 and remove CS from non-terminal set

#9: mutation length ML = max_permitted_depth - depht(mutation node)

#10: set current depth to 0, CD=0

#11: PP = production rules of CS
#L(CS ::= α) = length of the production rules CS
# must satisfy CD + L(CS ::= α) <= ML
# if PP is empty remove CS from X and return to step 8

#12: select 1 production from PP

#13: find production rules that satisfy
# (CD+1)+L(production rule) <= ML