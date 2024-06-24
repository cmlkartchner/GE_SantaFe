from agent import Agent
from constants import GRID_WIDTH, GRID_HEIGHT, EAST, NORTH, SOUTH, WEST
from grid_and_food import Grid
import numpy as np

def test_wrap_around_index():
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    a = Agent(grid)

    a.position = (0,0)
    a.heading = WEST
    assert a.convert_coords() == (grid.width - 1, 0)

    a.position = (0,0)
    a.heading = NORTH
    assert a.convert_coords() == (0, grid.height - 1)

def check_agent():
    # test an agent to make sure they're not sensing food they already touched
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    a = Agent(grid)
    a.phenotype = "if_food_ahead(prog2(move,left),left)"

    #if_food_ahead(prog2(move,left),left) --> [11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11. 11.
 #11. 11. 11. 11. 11. 11. 11.  0.]
    a.run_phenotype()


def build_agents():
    # builds 7 agents to represent population and assigns them num_food_eaten arrays
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    agents = []
    array1 = np.array([ 6,  6,  9, 11])
    array2 = np.array([ 0,  4,  6,  9])
    array3 = np.array([ 2,  4, 10, 21])
    array4 = np.array([ 2,  2, 14, 16])
    array5 = np.array([ 4,  5, 21, 23])
    array6 = np.array([15, 16, 17, 23])
    array7 = np.array([ 4,  5, 14, 16])
    arrays = [array1, array2, array3, array4, array5, array6, array7]

    for i in range(7):
        a = Agent(grid)
        a.amount_food_eaten = arrays[i]
        agents.append(a)

    return agents, grid

def test_novelty_score():
    agents, grid = build_agents()
    a = Agent(grid)
    a.amount_food_eaten = np.array([8, 8, 13, 18])
    a.novelty = a.novelty_score(agents, k=5)
    assert a.novelty == 8.368

test_novelty_score()

