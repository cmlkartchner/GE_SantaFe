class GGraph:
    # Todo: 
    # search by non terminal and return a node/value relative to the mod
    # create nodes based of dict
    def __init__(self) -> None:
        self.Nodes = []
        
    # return True if node is in graph
    def isNode(self, rule):
        for node in self.Nodes:
            if rule == node.get_value():
                return True
        return False
    
    def getNode(self, rule):
        for node in self.Nodes:
            if rule == node.get_value():
                return node
            
    # generates Graph
    def generateGraph(self, rules):
        # check if node exist in Graph
        for rule in rules:
            currNode = None
            if not self.isNode(rule):
                currNode = Node(rule)
                self.Nodes.append(currNode)
            else:
                currNode = self.getNode(rule)
            # create node for each non existant relative node and set in node list
            for relative in rules[rule]:
                relNode = None
                if not self.isNode(relative):
                    relNode = Node(relative)
                    self.Nodes.append(relNode)
                else:
                    relNode = self.getNode(relative)
                currNode.appendNode(relNode)
                
        # for every relative terminal node; increase weight
        # for every relative with weight decrease score
        # NOTE: right hand equivanance bias selection
        # NOTE: use geneotype for new termial selection? Node termaial non terminal lists?
        # TODO: think about weight calcuation; during/after?
        # NOTE: no repeative relative nodes
        # NOTE: update parents? because of recur
        pass
    def find_by_mod():
        pass
    def find_by_weight():
        pass

class Node:
    def __init__(self, inValue) -> None:
        # termial in this context means that there is no <> non terminals in the statement
        self.Nodes = []
        self.value = inValue
        if "<" not in inValue and ">" not in inValue:
            self.isTerminal = True
        else: 
            self.isTerminal = False
        self.weight = 0
    def appendNode(self, node):
        self.Nodes.append(node)
    def get_value(self):
        return self.value
    def find_mod_node():
        pass
    def find_weight_node():
        pass