from Agent import Agent
import numpy as np
import const as const

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
            neighboors = np.random.randint(const.GENERATION_LIMIT, size=const.NEIGHBOOR_SIZE)
            agent.sense(neighboors, self)
    def getAgent(self, num):
        pass