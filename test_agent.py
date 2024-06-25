from agent import Agent
from grid_and_food import Grid
from constants import GRID_WIDTH, GRID_HEIGHT
import numpy as np

def test_euclidean():
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    agent1 = Agent(grid=grid)
    agent2 = Agent(grid=grid)

    agent1.food_eaten_sequence = np.zeros((2,2))
    agent2.food_eaten_sequence = np.zeros((2,2))
    agent1.food_eaten_sequence[0] = (2,2)
    agent1.food_eaten_sequence[1] = (2,2)
    agent2.food_eaten_sequence[0] = (2,2)
    agent2.food_eaten_sequence[1] = (2,2)

    assert agent1.euclidean_distance(agent2, type="food_eaten_sequence") == 0

    agent1.food_eaten_sequence[0] = (1,2)
    agent1.food_eaten_sequence[1] = (3,4)

    agent2.food_eaten_sequence[0] = (5,6)
    agent2.food_eaten_sequence[1] = (7,8)

    assert agent1.euclidean_distance(agent2, type="food_eaten_sequence") == 8
