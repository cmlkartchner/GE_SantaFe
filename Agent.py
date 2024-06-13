import numpy as np
from ge_utils import Gene
import constants as constants

class Agent:
    def __init__(self, id) -> None:
        self.Gene = Gene(np.random.randint(101, size=constants.GENE_LEN))
        self.neighboorGeneList = []
        self.id = id
    def printID(self):
        print(f"{self.id}ID")
    def printGene(self):
        print(self.Gene.genotype)
    def printNeighboors(self):
        print(self.neighboorGeneList)
    def sense(self, neighboors, hiveMind):
        self.neighboorList.clear()
        for num in neighboors:
            self.neighboorGeneList.append(hiveMind.agentList[num].Gene.genotype)

        
class Space:
    def __init__(self) -> None:
        pass
            
        
        
        

# within grid it sense act update operation