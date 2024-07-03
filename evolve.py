from gene import Gene
import random
from agent import Agent, Food, Grid 
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES, NUM_AGENTS, DIVERSITY_CONSTANT, GENERATIONS
from evolve_manager import EvolveManager
import time
from datetime import datetime
import matplotlib.pyplot as plt
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

def write_highest_fitness(fitness_list):
    with open("highest_fitness.txt", "a") as fd:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fd.write(date + ",")
        for fitness in fitness_list:
            fd.write(str(fitness) + ",")
        fd.write("\n")
def create_graph(row_number):
    # row_number: line number in highest_fitness.txt, 1-indexed
    with open("highest_fitness.txt", "r") as fd:
        lines = fd.readlines()
        line = lines[row_number - 1]
        numbers = line.split(",")[1:-1] # skip first index
        numbers = [float(number) for number in numbers]
        plt.plot(numbers)
        plt.show()

# main evolution loop here
def evolve():
    best_fitness = [] # list of highest fitness values for each generation
    best_history = () # tuple of (best fitness, best history)

    evolve_manager = EvolveManager() # contains all the evolve functions
    grid = Grid(GRID_WIDTH, GRID_HEIGHT) # create ONLY one grid for all agents to share
    evolve_manager.generate_population(NUM_AGENTS, grid) # create population (stored within evolve_manager)
    grid.print_grid()

    # clear the files
    with open ("phenotypes.txt", "w") as _, open("fitness_values.txt", "w") as _:
        print("files cleared and ready for writing")

    for i in range(GENERATIONS): # each iteration is a 'generation'
        Gene.adjust_mutation_rate(i)
        new_population = [] # new population to replace the old one
        for agent in evolve_manager.population: # run the agents (must be complete before novelty can be calculated)
            agent.run_phenotype() # sets fitness

        # use num_food array from all agents to calculate novelty
        for agent in evolve_manager.population:
            #print("evolve loop", evolve_manager.population is None)
            agent.novelty = agent.novelty_score(population=evolve_manager.population) # set novelty score

        # sense-action-update loop
        for agent in evolve_manager.population:
            evolve_manager.sense(agent) # sample genotypes from neighbors
            new_agent = evolve_manager.act(agent) # mutate/crossover -> returns best gene produced
            new_population.append(evolve_manager.update(agent, new_agent))
        # compare diversity of the population (diversity metric of fitness function)
        #Agent.apply_diversity(new_population)
        # for agent in new_population:
        #     diff = agent.average_difference(new_population)/DIVERSITY_CONSTANT
        #     agent.gene.cost += diff
           
        # sort pop using updated costs
        evolve_manager.population = sorted(new_population[:], reverse=True, key=lambda x: x.gene.cost)

        #info for creating graphs of each generation
        best_fitness.append(evolve_manager.population[0].gene.cost) 

        # update the best agent
        if best_history == () or evolve_manager.population[0].gene.cost > best_history[0]:
            best_history = (evolve_manager.population[0].gene.cost, grid.history[evolve_manager.population[0].id].copy())

        # dynamic mutation (can't happen 1st generation)
        if len(best_fitness) > 1 and best_fitness[-1] == best_fitness[-2]:
            print("no improvement for", Gene.no_improvement_for, "generations")
            Gene.no_improvement_for += 1
        else: # the highest fitness changed (not necessarily increase/decrease)
            Gene.no_improvement_for = 0

        write_phenotypes(evolve_manager.population, i)
        write_fitness_to_file(evolve_manager.population)
        
        if i % 20 == 0:
            print("generation", i, " highest cost is ", evolve_manager.population[0].gene.cost)
            grid.print_history(evolve_manager.population[0])

    # print the best agent
    print("the cost of the best agent is", best_history[0])
    grid.print_history_base(best_history[1])
    write_highest_fitness(best_fitness)

evolve()
#create_graph(1)
