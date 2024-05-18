from ge_utils import Gene
import random
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES
from constants import NORTH, EAST, SOUTH, WEST

class Agent:
    def __init__(self, grid) -> None:
        # cost information
        self.food_touched = 0 # no duplicates
        self.distance = 0 # how far it has traveled (not displacement)

        # simulation information
        self.id = random.randint(0, 1000000)
        self.heading = NORTH
        self.position = (random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT)) # x,y BUT in the grid it is y,x
        self.grid = grid
        #self.grid.array[self.position[1]][self.position[0]] = self
        self.grid.update_history(self, self.position) # init with starting position

        # genetic information
        self.memory = [] # contains multiple genes
        self.gene = Gene([random.randint(0, 100) for i in range(GENE_LEN)])
        self.phenotype = self.gene.generate_phenotype(RULES, "<code>")

    # functions from the grammar
    def prog2(self, progs1, progs2):
        pass
        #print("prog2 is done") # all arguments are evaluated before calling
    def prog3(self, progs1, progs2, progs3):
        pass
        #print("prog3 is done") # all arguments are evaluated before calling
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
        #print("turned left")
        self.heading = (self.heading - 1) % 4
    def right(self):
        #print("turned right")
        self.heading = (self.heading + 1) % 4
    def move(self):
        #print("moved", self.heading)
        prev_position = self.position
        if self.heading == NORTH and self.grid.in_bounds(self.position[0],self.position[1] - 1):
            self.position = (self.position[0], self.position[1] - 1)
        elif self.heading == EAST and self.grid.in_bounds(self.position[0] + 1,self.position[1]):
            self.position = (self.position[0] + 1, self.position[1])
        elif self.heading == SOUTH and self.grid.in_bounds(self.position[0],self.position[1] + 1):
            self.position = (self.position[0], self.position[1] + 1)
        elif self.heading == WEST and self.grid.in_bounds(self.position[0] - 1,self.position[1]):
            self.position = (self.position[0] - 1, self.position[1])
        else: # did not move
            return
        
        # avoid double counting food
        if isinstance(self.grid.array[self.position[1]][self.position[0]], Food) and self.position not in self.grid.history[self.id]:
            self.food_touched += 1
        self.grid.update_history(self, self.position)
        self.distance += 1

    def if_food_ahead(self, arg1, arg2):
        #print("look for food ahead")
        if self.food_ahead() and callable(arg1):
            arg1()
        elif callable(arg2):
            arg2()
        # if the one is not callable then that means it was already called and evaluted to none
        # so no need to do anything extra
        # example case: if_food_ahead(left,prog2(move,move))

    def run_phenotype(self, phenotype):
        prog3 = self.prog3
        prog2 = self.prog2
        left = self.left
        right = self.right
        move = self.move
        if_food_ahead = self.if_food_ahead
        phenotype = phenotype.replace("left", "left||").replace("right", "right||").replace("move", "move||")
        # for if_food_ahead remove () for parameters inside function
        
        for i in range(len(phenotype)):
            if phenotype[i:].startswith("if_food_ahead"):
                left_index = phenotype.find("(", i)
                right_index = phenotype.find(")", i)
                fixed_string = phenotype[left_index:right_index].replace("|", "")
                phenotype = phenotype[:left_index] + fixed_string + phenotype[right_index:]
        phenotype = phenotype.replace("||", "()")

        eval(phenotype) # runs the program
        self.gene.cost = self.food_touched + self.distance / 100 # fitness function TODO: make better
    
    def __str__(self) -> str:
        return "A"

###### EVOLUTION 

class Food:
    def __init__(self, x, y) -> None:
        self.position = (x,y)
    def __str__(self) -> str:
        return "F"
class Grid:
    FOOD_NUM = 89
    OBSTACLE_PROB = 0
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.array = [[None for _ in range(width)] for _ in range(height)]
        self.add_food_and_obstacles(self.FOOD_NUM, self.OBSTACLE_PROB)
        self.history = {} # key: agent, value: set of positions agent has visited 

    def update_history(self, agent, position):
        if agent.id in self.history:
            self.history[agent.id].add(position)
        else:
            self.history[agent.id] = {position}

    def in_bounds(self,x,y):
        if self.width > x >= 0 and self.height > y >= 0:
            return True
        return False
    
    def add_food_and_obstacles(self, food_num, obstacle_prob):
        # add obstacles first so that they can't overwrite food
        # pick food_num spots and insert food

        # add obstacles
        for i in range(self.width):
            for j in range(self.height):
                if random.random() < obstacle_prob:
                    obstacle = Obstacle(i,j)
                    self.array[obstacle.position[1]][obstacle.position[0]] = obstacle

        # add food
        while food_num > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.array[y][x] is None:
                self.array[y][x] = Food(x, y)
                food_num -= 1
    
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
    
    def print_history(self, agent):
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
        

if __name__ == "__main__":
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    print("grid created")

    a = Agent(grid)
    grid.print_grid()
    a.phenotype = "prog3(move, left, move)"
    #"prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))"
    #"prog3(move, prog2(move, if_food_ahead(right,left)),move)"
    a.run_phenotype(a.phenotype)
    print("done running")
    grid.print_history(a)



# S###............................
# ...#............................
# ...#.....................###....
# ...#....................#....#..
# ...#....................#....#..
# ...####.#####........##.........
# ............#................#..
# ............#.......#...........
# ............#.......#........#..
# ............#.......#...........
# ....................#...........
# ............#................#..
# ............#...................
# ............#.......#.....###...
# ............#.......#..#........
# .................#..............
# ................................
# ............#...........#.......
# ............#...#..........#....
# ............#...#...............
# ............#...#...............
# ............#...#.........#.....
# ............#..........#........
# ............#...................
# ...##. .#####....#...............
# .#..............#...............
# .#..............#...............
# .#......#######.................
# .#.....#........................
# .......#........................
# ..####..........................
# ................................