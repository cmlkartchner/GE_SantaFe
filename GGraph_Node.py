class GGraph:
    # Todo: 
    # search by non terminal and return a node/value relative to the mod
    # create nodes based of dict
    def __init__(self) -> None:
        self.Nodes = []
        
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
            
    def find_by_mod(self, rule, codon):
        productions = self.getNode(rule).outNodes
        return productions[codon % len(productions)]
    
    def find_by_weight():
        # NOTE: use geneotype for new termial selection? Node termaial non terminal lists?
        pass
            
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
        self.outNodes.append(node)