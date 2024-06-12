# parse: vector through grammer to get code
from Agent import HiveMind 
import CONST as CONST

CurrHiveMind = HiveMind()
CurrHiveMind.generateAgents(CONST.GENERATION_LIMIT)
CurrHiveMind.printAgentIDs()
# run and test sense 