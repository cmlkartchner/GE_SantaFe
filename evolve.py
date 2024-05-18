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
    time.sleep(1)
    for i in range(300): # generations
        #for agent in evolve_manager.population:

        MAX_THREADS = len(evolve_manager.population) # Number of threads to use
        # Create a ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [] # Create a list to store the futures
            #for genome in population:
            i=0
            for agent in evolve_manager.population:
                if True: # ALTER to not run agent if same as prev...check
                    # Submit the task to the executor
                    print("submitting future ", i)
                    future = executor.submit(thread_routine, agent, evolve_manager)
                    print("future completed ", i)
                    futures.append(future) # Append the future object to the list
                    i+=1
            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
        evolve_manager.population = sorted(evolve_manager.population, reverse=True, key=lambda x: x.gene.cost)
        write_fitness_to_file(evolve_manager.population)
        
        if i % 20 == 0:
            print("generation", i, " highest cost is ", evolve_manager.population[0].gene.cost)
            grid.print_history(evolve_manager.population[0])

    # print the best agent
    best_agent = evolve_manager.population[0]
    print("the cost of the best agent is", best_agent.gene.cost)
    grid.print_history(best_agent)

evolve()
