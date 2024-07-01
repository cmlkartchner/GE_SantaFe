from constants import RULES
from gene import Gene
import numpy as np
class GGraph:
    def __init__(self, rules):
        self.Nodes = []
        self.generateGraph(rules)
        
    # return True if node is in graph
    def isNode(self, rule):
        for node in self.Nodes:
            if rule == node.value:
                return True
        return False
    
    def getNode(self, rule):
        for node in self.Nodes:
            if rule == node.value:
                return node
            
    # if node exist return if not create new
    def selectNode(self, header):
        if not self.isNode(header):
            currNode = Node(header)
            self.Nodes.append(currNode)
        else:
            currNode = self.getNode(header)
        return currNode
    
    # depth first traversal 
    def updateWeights(self, coreNode):
        for node in coreNode.inNodes:
            if node.weight < (coreNode.weight - 1):
                node.weight = coreNode.weight - 1
                self.updateWeights(node)
    
    # generates Graph
    def generateGraph(self, rules):
        # check if node exist in Graph
        for rule in rules:
            trunckNode = self.selectNode(rule)
            # create node for each non existant production node and set in node list
            terminalCount = 0
            for production in rules[rule]:
                branchNode = self.selectNode(production)
                if branchNode.isTerminal is True:
                    terminalCount += 1
                # set truck weight only if its more
                if trunckNode.weight < terminalCount:
                    trunckNode.weight = terminalCount    
                trunckNode.appendOutNode(branchNode)
                branchNode.appendInNode(trunckNode)
                self.updateWeights(branchNode)
            self.updateWeights(trunckNode)
    
    def printGraph(self):
        for node in self.Nodes:
            print(f'{node.value}:{node.weight}', [n.value for n in node.outNodes])
    
    def find_by_mod(self, rule, codon):
        productions = self.getNode(rule).outNodes
        return productions[codon % len(productions)].value
            
    def weight_traveral(self, Node, codon):
        if Node.isTerminal is True:
            return Node.value
        else:
            terminalPath = []
            # find available options
            for node in Node.outNodes:
                if node.isTerminal or (node.weight > Node.weight):
                    terminalPath.append(node)
            # NOTE: not all inculsive could still break with super 'cold' nodes
            if len(terminalPath) == 0:
                for node in Node.inNodes:
                    if node.isTerminal or (node.weight > Node.weight):
                        terminalPath.append(node)
            
            return self.weight_traveral(terminalPath[codon % len(terminalPath)], codon)  
        
    def find_by_weight(self, rule, codon):
        rootNode = self.getNode(rule)
        terminal = self.weight_traveral(rootNode, codon)
        return terminal

class Node:
    def __init__(self, inValue) -> None:
        # termial in this context means that there is no <> non terminals in the statement
        self.inNodes = []
        self.outNodes = []
        self.value = inValue
        if "<" not in inValue and ">" not in inValue:
            self.isTerminal = True
        else: 
            self.isTerminal = False
        self.weight = 0
    def appendOutNode(self, node):
        self.outNodes.append(node)
    def appendInNode(self, node):
        self.inNodes.append(node)

if __name__ == "__main__":
    ggraph = GGraph(RULES)
    ggraph.printGraph()
    print(ggraph.find_by_mod('<progs>', 32))
    print(ggraph.find_by_weight('<code>', 32))
    
    # genotype = [random.randint(0,100) for i in range(20)]
    # g = Gene(genotype)

    # ph = g.generate_phenotype2(GGraph(RULES), "<code>") 

    gene = Gene(np.random.randint(101, size=50))
    ggraph = GGraph(RULES)
    print(gene.generate_phenotype2(GGraph(RULES), '<code>'))


