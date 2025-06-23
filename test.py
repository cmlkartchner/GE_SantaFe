### TESTING ###
from santafe.santa_fe_utils import *

# world = SantaFe_World()
# # print(world.trail)
# # print(world.trail_start)

# # agent that will most likely fail
# # agent = SantaFe_Agent(Direction.WEST, world.trail_start, world, sim=None, gene=Gene(random.sample(range(1,1000), GENE_LEN)), id=0)
# # eval_fitness(agent)
# # print(agent.gene.phenotype)
# # print(agent.num_food_eaten)

# # agent that succeeds
# agent_succeed = SantaFe_Agent(Direction.WEST, world.trail_start, world, sim=None, gene=Gene([1, 3, 2]), id=1)
# eval_fitness(agent_succeed)
# # should just be "move"
# print(agent_succeed.gene.phenotype) # WORKS
# # should be 1
# print(agent_succeed.num_food_eaten) # WORKS
# for i in range(100): # should happen only like 1-3 times
#     mutate(agent_succeed.gene) # WORKS
# print(agent_succeed.gene.genotype)

# # agent that succeeds (but with longer gene)
# agent_long_succeed = SantaFe_Agent(Direction.WEST, world.trail_start, world, sim=None, gene=Gene([1, 1, 0, 3, 2, 3, 2]), id=2)
# # weirdly revealed bug where two agents can't share a single instance of world; need separate copies in order to not interfere with each other?
# eval_fitness(agent_long_succeed)
# print(agent_long_succeed.gene.phenotype) # should be prog2(move,move)
# print(agent_long_succeed.num_food_eaten)
# test_gene = Gene([1, 2, 3, 4, 5, 6])
# for i in range(10): # should trigger more than half the time
#     # Should be between 1 and 4
#     single_pt_crossover(agent_long_succeed.gene, test_gene) # WORKS

# # testing tournament select
# agents = []
# for i in range(10):
#     direction = random.choice(list(Direction))
#     pos = [random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)]
#     gene = Gene(random.sample(range(1,1000), 20))
#     agents.append(SantaFe_Agent(direction, pos, world, None, gene, i+3))
#     agents[i].num_food_eaten = random.randint(0, 10)
#     print(f"Agent {agents[i].id} num food eaten: {agents[i].num_food_eaten}")
#     # eval_fitness(agents[i]) # will work properly once the parser is fixed, but otherwise it works!
# agents.append(agent_succeed)
# agents.append(agent_long_succeed)

# # Tournament select works!
# winners = tournament_select(agents=agents)
# print("Tournament Winners:")
# for i in range(len(winners)):
#     print(f"Agent {winners[i].id} with {winners[i].num_food_eaten} food eaten")

### TESTING NSGA-II STUFF ###
dummy1 = SantaFe_Agent(Direction.EAST, id = 1) # should be rank 1, crowding dist = inf
dummy2 = SantaFe_Agent(Direction.WEST, id = 2) # should be lower rank than 1
dummy3 = SantaFe_Agent(Direction.NORTH, id = 3) # should be same rank as 2
dummy4 = SantaFe_Agent(Direction.SOUTH, id = 4) # should have lowest rank, crowding dist = inf

# non-dominance sorting
dummy1.num_food_eaten = 12
dummy1.num_moves_taken= 10

dummy2.num_food_eaten = 10
dummy2.num_moves_taken = 12

dummy3.num_food_eaten = 11
dummy3.num_moves_taken = 13

dummy4.num_food_eaten = 8
dummy4.num_moves_taken = 16

dummy_agents = [dummy1, dummy2, dummy3, dummy4]

# Non-domination sorting works!!!
ranked_solutions, solution_lookup = nondomination_sort(dummy_agents)
i = 1
for rank in ranked_solutions:
    print(f"RANK {i}")
    i += 1
    for solution in rank:
        print(f"Agent {solution.agent.id}: {solution.rank}")

food_eaten_sorted = sorted(dummy_agents, key=lambda x: x.num_food_eaten, reverse=False)
moves_taken_sorted = sorted(dummy_agents, key=lambda x: x.num_moves_taken, reverse=False)
print(f"Sorted by food eaten: {food_eaten_sorted}")
print(f"Sorted by moves taken: {moves_taken_sorted}")

# testing crowding distance calculations
# dummy1 and dummy4 crowding distance should be inf dist
calculate_crowding_dist(dummy_agents, solution_lookup)
for rank in ranked_solutions:
    for solution in rank:
        print(f"Agent {solution.agent.id} crowding dist: {solution.crowding_dist}")

# agent 2 crowding dist = 0
# agent 3 crowding dist = 1
winner = pareto_tournament([dummy2, dummy3], solution_lookup)
print(f"Winner: Agent {winner.id}") # should be agent 2

winner = pareto_tournament(dummy_agents, solution_lookup)
print(f"Winner: Agent {winner.id}") # should be agent 1
