from agent import Agent
import numpy as np
import constants as constants

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
            neighboors = np.random.randint(constants.GENERATION_LIMIT, size=constants.NEIGHBOOR_SIZE)
            agent.sense(neighboors, self)
    def getAgent(self, num):
        pass
    
class EndException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)