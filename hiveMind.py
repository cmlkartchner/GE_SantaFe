from Agent import Agent
import numpy as np
from Grid_Food_EndExpect import Grid
import const as const

class HiveMind:
    def __init__(self, numAgents):
        self.agentList = []
        for i in range(numAgents):        
            grid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT)
            self.agentList.append(Agent(grid, i))
            
    def printAgentIDs(self):
        for agent in self.agentList:
            agent.printID()
            
    def initiateSense(self):
        for agent in self.agentList:
            neighboorsPosition = np.random.randint(const.GENERATION_LIMIT, size=const.NEIGHBOOR_SIZE)
            neighboorsAgents = []
            for num in neighboorsPosition:
                neighboorsAgents.append(self.agentList[num])
            agent.sense(neighboorsAgents, self)
            
    def initiateActUpdate(self):
        for agent in self.agentList:
            agent.actUpdate()
            
    def write_fitness_to_file(self):
        with open("fitness_values.txt", "a") as fd:
            for agent in self.agentList:
                fd.write(str(round(agent.gene.cost, 4)) + ", ")
            fd.write("\n")

    # write the phenotypes of the population to a file
    def write_phenotypes(self, num):
        with open("phenotypes.txt", "a") as fd:
            fd.write("Generation: " + str(num) + "\n")
            for agent in self.agentList:
                fd.write(agent.phenotype + "\n")
                fd.flush()
            fd.write("\n")