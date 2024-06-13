# parse: vector through grammer to get code
from hiveMind import HiveMind 
import constants as constants

CurrHiveMind = HiveMind()
CurrHiveMind.generateAgents(constants.GENERATION_LIMIT)
CurrHiveMind.printAgentIDs()
# run and test sense 