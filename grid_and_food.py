import random
from constants import GRID_HEIGHT, GRID_WIDTH, THE_GRID, FOOD_NUM

class Food:
    def __init__(self, x, y) -> None:
        self.position = (x,y)
    def __str__(self) -> str:
        return "F"
class Grid:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.array = [[None for _ in range(width)] for _ in range(height)] #the grid
        self.add_food_specific_map(THE_GRID) # fill grid with food based on the map saved in constants.py
        self.history = {} # key: agent, value: set of positions agent has visited 

    def update_history(self, agent, position): # update history dictionary for a particular agent
        if agent.id in self.history:
            self.history[agent.id].add(position)
        else:
            self.history[agent.id] = {position}

    def in_bounds(self,x,y): # not in use since grid is circular
        if self.width > x >= 0 and self.height > y >= 0:
            return True
        return False
    
    def add_food_random(self, food_num): # not in use since we are using a specific map
        # add obstacles first so that they can't overwrite food
        # pick food_num spots and insert food

        # add food
        while food_num > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.array[y][x] is None:
                self.array[y][x] = Food(x, y)
                food_num -= 1
    
    def add_food_specific_map(self, food_map):
        # food_map: a string representation of the grid (found in constants.py)
        rows = food_map.split("\n")
        rows = [row.strip() for row in rows if row.strip() != ""]
        self.width = len(rows[0])
        self.height = len(rows)
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == "#":
                    self.array[i][j] = Food(j, i)

    def color(self, item):
        return "\x1b[33m" + str(item) +"\x1b[0m"
    
    def print_grid(self): # if bold = True, an agent must be specified 
        for row in self.array:
            row_str = ""
            for item in row:
                if item is None:
                    row_str += "."
                else:
                    row_str += str(item)
            print(row_str)
    
    def print_history(self, agent): # print the grid with the agent's path in yellow
        positions = self.history[agent.id]
        for i in range(self.height): # y
            row_str = ""
            for j in range(self.width): # x
                if (j,i) in positions: # BOLD CASE
                    if self.array[i][j] is None:
                        row_str += self.color(".")
                    else:
                        row_str += self.color(self.array[i][j])

                else: #Non-bold case
                    if self.array[i][j] is None:
                        row_str += "."
                    else:
                        row_str += str(self.array[i][j])
            print(row_str)