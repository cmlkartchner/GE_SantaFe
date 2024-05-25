from ge_utils import Gene
import random
from agent import Agent, Food, Grid 
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES, NUM_AGENTS
from evolve_manager import EvolveManager
# no out of bounds in the grid
import time
import threading
import concurrent.futures

# this is master which should import basically all other files

# create the agents
# generate population means...create a bunch of agents (creating agents creates the genes too)

# go through every agent, 
def write_fitness_to_file(population):
    with open("fitness_values.txt", "a") as f:
        for agent in population:
            f.write(str(round(agent.gene.cost, 4)) + ", ")
        f.write("\n")


def write_phenotypes(population, i):
    with open("phenotypes.txt", "a") as f:
        f.write("Generation: " + str(i) + "\n")
        for agent in population:
            f.write(agent.phenotype + "\n")
        f.write("\n")

#NOT IN USE..potentially to add in threading at another time
def thread_routine(agent, evolve_manager):
    agent.run_phenotype(agent.phenotype)
    print("run")
    # run agent program 1 time, then do sense, act, update
    evolve_manager.sense(agent)
    new_gene = evolve_manager.act(agent) # returns best gene produced
    print("act done")
    agent.gene = evolve_manager.update(agent.gene, new_gene) # update gene if better

    agent.phenotype = agent.gene.generate_phenotype(RULES, "<code>") # generate in case it changed
    print("routine completed")
# race conditions KT?
# hmmm but an agent only updates it's gene once it is done, no agents ever deleted
# each thread is only editing itself so they'll never edit the same thing at the same time

def evolve():
    evolve_manager = EvolveManager()
    grid = Grid(GRID_WIDTH, GRID_HEIGHT) # create ONLY one grid
    evolve_manager.generate_population(NUM_AGENTS, grid) # create population
    grid.print_grid()

    for i in range(100): # generations
        new_population = []
        for agent in evolve_manager.population:
            agent.run_phenotype(agent.phenotype) # run program 
            evolve_manager.sense(agent) # sample neighbors
            new_agent = evolve_manager.act(agent) # returns best gene produced
            new_population.append(evolve_manager.update(agent, new_agent))

        # sort population based on updated costs
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
