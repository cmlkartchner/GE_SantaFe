# parse: vector through grammer to get code
from HiveMind import HiveMind 
import const as const

const.DIVERSITY = const.Base_DIVERSITY
const.FOOD_INCENTIVE = const.Base_FOOD_INCENTIVE
const.CONSECUTIVE_FOOD = const.Base_CONSECUTIVE_FOOD
const.DISTANCEPINCH = const.Base_DISTANCEPINCH
const.MUTATION_RATE = const.Base_MUTATION_RATE
const.OFFPATHPENALTY = const.Base_OFFPATHPENALTY

CurrHiveMind = HiveMind(const.POPULATION_LIMIT)
with open("fitness_values.txt", "a") as fd:
    fd.write("Attempt Start \n")

with open("genotypes.txt", "a") as fd:
    fd.write("Attempt Start \n")

maxHeighest = 0
for num in range(const.GENERATIONS + 1):
    CurrHiveMind.initiateSense()
    CurrHiveMind.initiateActUpdate()
    CurrHiveMind.write_fitness_to_file()
    # CurrHiveMind.write_genotypes()
    mostFit = CurrHiveMind.getStrongestAgent()
    mostFull = CurrHiveMind.getMostFullAgent()
    mostFit.run_phenotype()
    mostFull.run_phenotype()
    if mostFull.food_touched > maxHeighest:
        maxHeighest = mostFull.food_touched
    with open("fitness_values.txt", "a") as fd:
        fd.write(f"gen{num} highest {mostFit.id} food touched: {mostFit.food_touched} Score: {mostFit.gene.cost} Production: {CurrHiveMind.projectionTally} mutate: {CurrHiveMind.mutateTally}")
        fd.write('\n')
        fd.write(f"gen{num} highest {mostFull.id} food touched: {mostFull.food_touched} Score: {mostFull.gene.cost} Production: {CurrHiveMind.projectionTally} mutate: {CurrHiveMind.mutateTally}")
        fd.write('\n')
    with open("phenotypes.txt", "a") as fd:
        fd.write(f"Gen{num} stat: currcon;{const.CONSECUTIVE_FOOD} currpen;{const.OFFPATHPENALTY} currins;{const.FOOD_INCENTIVE} dist;{mostFull.distance} offP;{mostFull.offPath} cons;{mostFull.consecutiveFood} food;{mostFull.food_touched}")
        fd.write('\n')
        fd.write(f"{mostFull.gene.genotype}")
        fd.write('\n')
        fd.write(mostFull.phenotype)
        fd.write('\n')
        fd.write(CurrHiveMind.grid.printed_history(mostFull))
        fd.write('\n')
    # CurrHiveMind.dynamicFitnessCheckAll()
    # CurrHiveMind.reassessFitnesses()
        
with open("fitness_values.txt", "a") as fd:
    fd.write(f"\n Attempt done; max fit {maxHeighest}")
    fd.write('\n')

# main evolution loop here
# def evolve():
#     # evolve_manager = EvolveManager() # contains all the evolve functions
#     grid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT) # create ONLY one grid for all agents to share
#     # evolve_manager.generate_population(NUM_AGENTS, grid) # create population (stored within evolve_manager)
#     grid.print_grid()

#     # clear the files
#     with open ("phenotypes.txt", "w") as _, open("fitness_values.txt", "w") as _:
#         print("files cleared and ready for writing")

#     for i in range(GENERATIONS): # each iteration is a 'generation'
#         new_population = [] # new population to replace the old one
#         # for agent in evolve_manager.population:
#             agent.run_phenotype(evolve_manager.population) # run program 
#             evolve_manager.sense(agent) # sample genotypes from neighbors
#             new_agent = evolve_manager.act(agent) # mutate/crossover -> returns best gene produced
#             new_population.append(evolve_manager.update(agent, new_agent))

#         # compare diversity of the population (diversity metric of fitness function)
#         Agent.apply_diversity(new_population)
#         # for agent in new_population:
#         #     diff = agent.average_difference(new_population)/DIVERSITY_CONSTANT
#         #     agent.gene.cost += diff
           
#         # sort pop using updated costs
#         evolve_manager.population = sorted(new_population[:], reverse=True, key=lambda x: x.gene.cost)
#         write_phenotypes(evolve_manager.population, i)
#         write_fitness_to_file(evolve_manager.population)
        
#         if i % 20 == 0:
#             print("generation", i, " highest cost is ", evolve_manager.population[0].gene.cost)
#             grid.print_history(evolve_manager.population[0])

#     # print the best agent
#     best_agent = evolve_manager.population[0]
#     print("the cost of the best agent is", best_agent.gene.cost)
#     grid.print_history(best_agent)