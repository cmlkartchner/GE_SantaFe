from ge_utils import Gene
import random
from agent import Agent, Food, Grid 
from constants import GENE_LEN, GRID_SIZE, RULES, NUM_AGENTS
from evolve_manager import EvolveManager
# no out of bounds in the grid
import time

# this is master which should import basically all other files

# create the agents
# generate population means...create a bunch of agents (creating agents creates the genes too)

# go through every agent, 
def write_fitness_to_file(population):
    with open("fitness_values.txt", "a") as f:
        for agent in population:
            f.write(str(round(agent.gene.cost, 4)) + ", ")
        f.write("\n")


def evolve():
    evolve_manager = EvolveManager()
    grid = Grid(GRID_SIZE, GRID_SIZE) # create ONLY one grid
    evolve_manager.generate_population(NUM_AGENTS, grid) # create population
    grid.print_grid()
    time.sleep(2)
    for i in range(300): # generations
        for agent in evolve_manager.population:
            # run agent
            agent.run_phenotype(agent.phenotype)
            # print("HISTORY OF AGENT", agent.id)
            # grid.print_history(agent) # print the history of the agent (where it has been
            # time.sleep(3)
            # run agent program 1 time, then do sense, act, update
            evolve_manager.sense(agent)
            new_gene = evolve_manager.act(agent.gene, agent) # returns best gene produced
            agent.gene = evolve_manager.update(agent.gene, new_gene) # update gene if better
            agent.phenotype = agent.gene.generate_phenotype(RULES, "<code>") # generate in case it changed

        write_fitness_to_file(evolve_manager.population)

    # print the best agent
    best_agent = sorted(evolve_manager.population, key=lambda x: x.gene.cost)[0]
    grid.print_history(best_agent)

evolve()
