import numpy as np
from ge_utils import Gene
import CONST as CONST

class Agent:
    def __init__(self, id) -> None:
        self.Gene = Gene(np.random.randint(101, size=CONST.GENE_LEN))
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
        
class HiveMind:
    def __init__(self) -> None:
        self.agentList = []
    def generateAgents(self, numAgents):
        for i in range(numAgents):
            self.agentList.append(Agent(i))
    def printAgentIDs(self):
        for agent in self.agentList:
            agent.printID()
    def printAgentMemory(self):
        for agent in self.agentList:
            agent.printNeighboors()
    def initiateSense(self):
        for agent in self.agentList:
            neighboors = np.random.randint(CONST.GENERATION_LIMIT, size=CONST.NEIGHBOOR_SIZE)
            agent.sense(neighboors, self)
    def getAgent(self, num):
        pass
        
class Space:
    def __init__(self) -> None:
        pass
            
        
        
        

# within grid it sense act update operation