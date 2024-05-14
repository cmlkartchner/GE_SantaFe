
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
GRID_SIZE = 30
# coord
import random
class agent:
    def __init__(self, grid) -> None:
        # cost information
        self.food_touched = 0 # no duplicates
        self.distance = 0 # how far it has traveled (not displacement)

        # simulation information
        self.id = 0
        self.heading = NORTH
        self.position = (0, 0) # x,y BUT in the grid it is y,x
        self.grid = grid
        self.grid.array[self.position[1]][self.position[0]] = self

        # genetic information
        self.memory = [] # contains multiple genes
        self.gene = None
        self.phenotype = None

    # functions from the grammar
    def prog2(self, progs1, progs2):
        print("prog2 is done") # all arguments are evaluated before calling
    def prog3(self, progs1, progs2, progs3):
        print("prog3 is done") # all arguments are evaluated before calling
    def food_ahead(self):
        # check if there is food in front of the agent
        if self.heading == NORTH:
            return self.grid.in_bounds(self.position[0],self.position[1] - 1) and isinstance(self.grid.array[self.position[1]-1][self.position[0]], Food)
        elif self.heading == EAST:
            return self.grid.in_bounds(self.position[0] + 1,self.position[1]) and isinstance(self.grid.array[self.position[1]][self.position[0] + 1], Food)
        elif self.heading == SOUTH:
            return self.grid.in_bounds(self.position[0],self.position[1] + 1) and isinstance(self.grid.array[self.position[1] + 1][self.position[0]], Food)
        elif self.heading == WEST:
            return self.grid.in_bounds(self.position[0] - 1,self.position[1]) and isinstance(self.grid.array[self.position[1]][self.position[0] - 1], Food)

    def left(self):
        print("turned left")
        self.heading = (self.heading - 1) % 4
    def right(self):
        print("turned right")
        self.heading = (self.heading + 1) % 4
    def move(self):
        print("moved")
        prev_position = self.position
        if self.heading == NORTH and self.grid.in_bounds(self.position[0],self.position[1] - 1):
            self.position = (self.position[0], self.position[1] - 1)
        elif self.heading == EAST and self.grid.in_bounds(self.position[0] + 1,self.position[1]):
            self.position = (self.position[0] + 1, self.position[1])
        elif self.heading == SOUTH and self.grid.in_bounds(self.position[0],self.position[1] + 1):
            self.position = (self.position[0], self.position[1] + 1)
        elif self.heading == WEST and self.grid.in_bounds(self.position[0] - 1,self.position[1]):
            self.position = (self.position[0] - 1, self.position[1])

        self.grid.array[self.position[1]][self.position[0]] = self # move agent to new position
        self.grid.array[prev_position[1]][prev_position[0]] = 0

    def if_food_ahead(self, arg1, arg2):
        print("look for food ahead")
        if self.food_ahead():
            arg1()
        else:
            arg2()

    def run_phenotype(self, phenotype):
        left = agent.left
        right = agent.right
        move = agent.move
        if_food_ahead = agent.if_food_ahead
        phenotype = phenotype.replace("left", "left||").replace("right", "right||").replace("move", "move||")
        # for if_food_ahead remove () for parameters inside function
        
        for i in range(len(phenotype)):
            if phenotype[i:].startswith("if_food_ahead"):
                left_index = phenotype.find("(", i)
                right_index = phenotype.find(")", i)
                fixed_string = phenotype[left_index:right_index].replace("|", "")
                phenotype = phenotype[:left_index] + fixed_string + phenotype[right_index:]
        phenotype = phenotype.replace("||", "()")
        return eval(phenotype)
    
    def __str__(self) -> str:
        return "A"

    #run_phenotype("prog3(move, prog2(move, if_food_ahead(right,left)),move)")

class Food:
    def __init__(self, x, y) -> None:
        self.position = (x,y)
    def __str__(self) -> str:
        return "F"

class Obstacle:
    def __init__(self, x, y) -> None:
        self.position = (x, y)
    def __str__(self) -> str:
        return "O"

class Grid:
    FOOD_PROB = 0.2
    OBSTACLE_PROB = 0.05
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.array = [[None for _ in range(width)] for _ in range(height)]
        self.add_food_and_obstacles(self.FOOD_PROB, self.OBSTACLE_PROB)

    def in_bounds(self,x,y):
        if self.width > x >= 0 and self.height > y >= 0:
            return True
        return False
    
    def add_food_and_obstacles(self, food_prob, obstacle_prob):
        # 20

        # pick food_num spots and insert food
        for i in range(self.width):
            for j in range(self.height):
                chance = random.random()
                if chance < food_prob: #20% 
                    food = Food(i,j)
                    self.array[food.position[1]][food.position[0]] = food
                elif chance < food_prob + obstacle_prob:
                    obstacle = Obstacle(i,j)
                    self.array[obstacle.position[1]][obstacle.position[0]] = obstacle
        
    def print_grid(self):
        for row in self.array:
            row_str = ""
            for item in row:
                if item is None:
                    row_str += "."
                else:
                    row_str += str(item)
            print(row_str)

    


if __name__ == "__main__":
    grid = Grid(GRID_SIZE, GRID_SIZE)
    print("grid created")


    a = agent(grid)
    grid.print_grid()
    a.phenotype = "prog3(move, prog2(move, if_food_ahead(right,left)),move)"
    a.run_phenotype(a.phenotype)
    # print(a.food_ahead())
    # a.left()
    # a.move()
    # print(a.food_ahead())
    # a.right()