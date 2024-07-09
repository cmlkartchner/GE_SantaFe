
from Agent import Agent
import numpy as np
from GGraph_Node import GGraph
from Grid_Food_EndExpect import Grid
import const

class HiveMind:
    def __init__(self, numAgents):
        self.agentList = []
        self.projectionTally = 0
        self.mutateTally = 0
        self.rules = GGraph(const.RULES)
        self.grid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT)
        for i in range(numAgents):        
            self.agentList.append(Agent(self.grid, self.rules, id=i))
            
    def printAgentIDs(self):
        for agent in self.agentList:
            agent.printID()
        
    def getStrongestAgent(self):
        strongAgent = self.agentList[0]
        for agent in self.agentList:
            if strongAgent.gene.cost < agent.gene.cost:
                strongAgent = agent
        return strongAgent

    def getMostFullAgent(self):
        strongAgent = self.agentList[0]
        for agent in self.agentList:
            if strongAgent.food_touched < agent.food_touched:
                strongAgent = agent
        return strongAgent
            
    def initiateSense(self):
        for agent in self.agentList:
            neighboorsPosition = np.random.randint(const.POPULATION_LIMIT, size=const.NEIGHBOOR_SIZE)
            neighboorsAgents = []
            for num in neighboorsPosition:
                neighboorsAgents.append(self.agentList[num])
            agent.sense(neighboorsAgents)
            
    def initiateActUpdate(self):
        self.projectionTally = 0
        self.mutateTally = 0
        for agent in self.agentList:
            agent.actUpdate()
            self.projectionTally += agent.projectionresult
            self.mutateTally += agent.mutateresult
            
    def dynamicFitnessCheckAll(self):
        aboveThreshold = 0
        belowThreshold = 0
        for agent in self.agentList:
            if agent.consecutiveFood > (const.FITNESS_FOOD_UPPER_THRESHOLD * agent.food_touched):
                aboveThreshold += 1
            elif agent.consecutiveFood < (const.FITNESS_FOOD_LOWER_THRESHOLD * agent.food_touched):
                belowThreshold += 1
        if aboveThreshold > belowThreshold and aboveThreshold > (len(self.agentList) * .5):
            const.CONSECUTIVE_FOOD = np.round((const.CONSECUTIVE_FOOD * const.CONSEC_RATE_DECREASE), 2)
        elif aboveThreshold < belowThreshold and belowThreshold > (len(self.agentList) * .5):
            const.CONSECUTIVE_FOOD = np.round((const.CONSECUTIVE_FOOD * const.CONSEC_RATE_INCREASE), 2)
        # for agent in self.agentList:
        #     if agent.offPath > (const.FITNESS_PEN_UPPER_THRESHOLD * agent.distance):
        #         aboveThreshold += 1
        #     elif agent.offPath < (const.FITNESS_PEN_LOWER_THRESHOLD * agent.distance):
        #         belowThreshold += 1
        # if aboveThreshold > belowThreshold and aboveThreshold > (len(self.agentList) * .5):
        #     const.OFFPATHPENALTY = np.round((const.OFFPATHPENALTY * const.PENALTY_RATE_INCREASE), 2)
        # elif aboveThreshold < belowThreshold and belowThreshold > (len(self.agentList) * .5):
        #     const.OFFPATHPENALTY = np.round((const.OFFPATHPENALTY * const.PENALTY_RATE_DECREASE), 2)
            
    
    def dynamicFitnessCheck(self, topAgent):
        if topAgent.offPath > (const.FITNESS_PEN_UPPER_THRESHOLD * topAgent.distance):
            const.OFFPATHPENALTY = np.round((const.OFFPATHPENALTY * const.PENALTY_RATE_INCREASE), 2)
        elif topAgent.offPath < (const.FITNESS_PEN_LOWER_THRESHOLD * topAgent.distance):
            const.OFFPATHPENALTY = np.round((const.OFFPATHPENALTY * const.PENALTY_RATE_DECREASE), 2)
        # if topAgent.consecutiveFood > (const.FITNESS_FOOD_UPPER_THRESHOLD * topAgent.food_touched):
        #     const.CONSECUTIVE_FOOD = np.round((const.CONSECUTIVE_FOOD * const.CONSEC_RATE_DECREASE), 2)
        # elif topAgent.consecutiveFood < (const.FITNESS_FOOD_LOWER_THRESHOLD * topAgent.distance):
        #     const.CONSECUTIVE_FOOD = np.round((const.CONSECUTIVE_FOOD * const.CONSEC_RATE_INCREASE), 2)
            
    def reassessFitnesses(self):
        for agent in self.agentList:
            agent.run_phenotype()
            
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
        
    def write_genotypes(self):
        with open("genotypes.txt", "a") as fd:
            for agent in self.agentList:
                fd.write(f"{agent.id}:{agent.gene.cost} {agent.gene.genotype} \n")
            fd.write("\n")