from gene import Gene
import random
from agent import Agent, Food, Grid 
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES, NUM_AGENTS, DIVERSITY_CONSTANT, GENERATIONS
from evolve_manager import EvolveManager
import time

# master class: call python3 evolve.py to run

# write the fitness values of the population to a file
def write_fitness_to_file(population):
    with open("fitness_values.txt", "a") as fd:
        for agent in population:
            fd.write(str(round(agent.gene.cost, 4)) + ", ")
        fd.write("\n")

# write the phenotypes of the population to a file
def write_phenotypes(population, i):
    with open("phenotypes.txt", "a") as fd:
        fd.write("Generation: " + str(i) + "\n")
        for agent in population:
            fd.write(agent.phenotype + "\n")
            fd.flush()
        fd.write("\n")

# main evolution loop here
def evolve():
    evolve_manager = EvolveManager() # contains all the evolve functions
    grid = Grid(GRID_WIDTH, GRID_HEIGHT) # create ONLY one grid for all agents to share
    evolve_manager.generate_population(NUM_AGENTS, grid) # create population (stored within evolve_manager)
    grid.print_grid()

    # clear the files
    with open ("phenotypes.txt", "w") as _, open("fitness_values.txt", "w") as _:
        print("files cleared and ready for writing")

    for i in range(GENERATIONS): # each iteration is a 'generation'
        new_population = [] # new population to replace the old one
        for agent in evolve_manager.population:
            agent.run_phenotype(evolve_manager.population) # run program 
            evolve_manager.sense(agent) # sample genotypes from neighbors
            new_agent = evolve_manager.act(agent) # mutate/crossover -> returns best gene produced
            new_population.append(evolve_manager.update(agent, new_agent))

        # compare diversity of the population (diversity metric of fitness function)
        # for agent in new_population:
        #     diff = agent.average_difference(new_population)/DIVERSITY_CONSTANT
        #     agent.gene.cost += diff
           
        # sort pop using updated costs
        evolve_manager.population = sorted(new_population[:], reverse=True, key=lambda x: x.gene.cost)
        write_phenotypes(evolve_manager.population, i)
        write_fitness_to_file(evolve_manager.population)
        
        if i % 20 == 0:
            print("generation", i, " highest cost is ", evolve_manager.population[0].gene.cost)
            grid.print_history(evolve_manager.population[0])

    # print the best agent
    best_agent = evolve_manager.population[0]
    print("the cost of the best agent is", best_agent.gene.cost)
    grid.print_history(best_agent)


evolve()
