class GGraph:
    # Todo: 
    # search by non terminal and return a node/value relative to the mod
    # create nodes based of dict
    def __init__(self) -> None:
        self.Nodes = []
    def generateGraph(self, rules):
        # create core node
        # loop or recursive? recur; doesn't recur on existing nodes and terminal
        # at every option, need to find all non termials that for option and make nodes
        # check if node exist in Graph
        # create node for each non existant relative node and set in node list
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
    def __init__(self) -> None:
        # termial in this context means that there is no <> non terminals in the statement
        self.Nodes = []
        self.value = ''
        self.isTerminal = False
        self.weight = 0
    def find_mod_node():
        pass
    def find_weight_node():
        pass
    
    