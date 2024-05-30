from ge_utils import Gene
import random
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES, THE_GRID, FOOD_NUM
from constants import NORTH, EAST, SOUTH, WEST
from end_exception import EndException
from copy import deepcopy
class Agent:
    def __init__(self, grid, gene=None, id=None) -> None:
        # cost information
        self.food_touched = 0 # no duplicates
        self.distance = 0 # how far it has traveled (not displacement)
        self.moves = 0 # how many actions: left, right, move

        # simulation information
        if id is None:
            self.id = random.randint(0, 1000000)
        else:
            self.id = id

        self.heading = NORTH
        self.position = (0,0)
        #(random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT)) # x,y BUT in the grid it is y,x
        
        self.grid = grid
        
        self.grid.update_history(self, self.position) # init with starting position

        # genetic information
        self.memory = [] # contains multiple genes

        if gene is None: # allow us to manually insert genes in order to 'test' random ones during act function
            self.gene = Gene([random.randint(0, 100) for i in range(GENE_LEN)])
        else:
            self.gene = deepcopy(gene)
        self.phenotype = self.gene.generate_phenotype(RULES, "<code>")

        self.index = 0
        self.func = None # parsed list of functions representing the current phenotype
        self.terminal_functions_run = 0

    # functions from the grammar
    def prog2(self, progs1, progs2):
        progs1()
        progs2()

    def prog3(self, progs1, progs2, progs3):
        progs1()
        progs2()
        progs3()

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
        if self.should_end():
            self.end()
        self.moves+=1
        self.heading = (self.heading - 1) % 4
    def right(self):
        if self.should_end():
            self.end()
        self.moves+=1
        self.heading = (self.heading + 1) % 4
    def move(self):
        if self.should_end():
            self.end()
        self.moves+=1

        if self.heading == NORTH:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.heading == EAST:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.heading == SOUTH:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.heading == WEST:
            self.position = (self.position[0] - 1, self.position[1])
        else: # did not move
            return
        
        # circular grid with no ending
        if self.position[0] >= GRID_WIDTH:
            self.position = (0, self.position[1])
        elif self.position[0] == -1:
            self.position = (GRID_WIDTH - 1, self.position[1])
        
        if self.position[1] >= GRID_HEIGHT:
            self.position = (self.position[0], 0)
        elif self.position[1] == -1:
            self.position = (self.position[0], GRID_HEIGHT - 1)

        # avoid double counting food
        if isinstance(self.grid.array[self.position[1]][self.position[0]], Food) and self.position not in self.grid.history[self.id]:
            self.food_touched += 1
        self.grid.update_history(self, self.position)
        self.distance += 1

    def if_food_ahead(self, arg1, arg2):
        if self.food_ahead():
            arg1()
        else:
            arg2()

    # functions for ending the simulation
    def should_end(self):
        self.terminal_functions_run += 1
        if self.food_touched == FOOD_NUM or self.moves == 400 or self.terminal_functions_run == 1000:
            return True
        return False
    def end(self):
        raise EndException("End of simulation")

    def append_lambda(self, args, arguments, type): # IMPORTANT ADDITION TO FIX WEIRD LAMBDA ERRORS
        # Capture current values of arguments[0] and arguments[1]
        arg1, arg2 = arguments[0], arguments[1]
        if type == "if_food_ahead":
            args.append(lambda: self.if_food_ahead(arg1, arg2))
        elif type == "prog2":
            args.append(lambda: self.prog2(arg1, arg2))
        elif type == "prog3":
            arg3 = arguments[2]
            args.append(lambda: self.prog3(arg1, arg2, arg3))

    def get_arg(self, num_args): # returns a list of lambda functions
        # starting at index
        args = [] # holds num_args lambda functions
        while num_args > 0:
            if self.func[self.index] in ["move", "left", "right"]:
                if self.func[self.index] == "move":
                    args.append(lambda: self.move())
                elif self.func[self.index] == "left":
                    args.append(lambda: self.left())
                elif self.func[self.index] == "right":
                    args.append(lambda: self.right())
                self.index+=1

            elif self.func[self.index] == "if_food_ahead":
                self.index+=1
                arguments = self.get_arg(2)
                self.append_lambda(args, arguments, "if_food_ahead")

            elif self.func[self.index] == "prog2":
                self.index+=1
                arguments = self.get_arg(2)
                self.append_lambda(args, arguments, "prog2")
            
            elif self.func[self.index] == "prog3":
                self.index+=1
                arguments = self.get_arg(3)
                self.append_lambda(args, arguments, "prog3")
            else:
                print("Error: function not found")
            num_args -= 1
        
        return args
    
    def parse_phenotype(self):
        # parse the phenotype into a list of functions to call get_args on
        self.func = self.phenotype.replace("(", " ").replace(")", " ").replace(",", " ").split()
    
    def diversity(self, agent1_func, agent2_func):
        # calculate the diversity between two agents
        # number of differences in genotype
        assert agent1_func != None, "Phenotype not parsed yet"
        assert agent2_func != None, "Phenotype not parsed yet"

        difference = abs(len(agent1_func) - len(agent2_func)) # difference in length
        for i in range(min(len(agent1_func), len(agent2_func))):
            if agent1_func[i] != agent2_func[i]:
                difference += 1
        return difference
    
    def average_difference(self, population=None):
        # compare agent with all the other agents and return its average difference, aka, DIVERSITY
        if population is None:
            return 0 # off switch for when you don't have a population to calculate against
        return sum(self.diversity(self.func, agent.func) for agent in population) / len(population)
    
    def run_phenotype(self, population):
        # repeatedly run the phenotype until the should_end is true
        try:
            self.grid.history[self.id] = set() # reset before running again
            self.moves = 0
            self.food_touched = 0
            self.distance = 0
            self.terminal_functions_run = 0
            self.position = (0,0)
            while(True):
                self.run_phenotype_once()
        except EndException as e:
            self.gene.cost = self.food_touched + self.distance / 100 + self.average_difference(population)/100
            #TODO: how big should the diversity addition be? 
            #print("cost: ", self.phenotype, "\n->", self.gene.cost)

    def run_phenotype_once(self):
        left = self.left
        right = self.right
        move = self.move
        self.parse_phenotype() # set self.func to parsed phenotype
        self.index = 1 # skip the first function

        if self.func[0] == "if_food_ahead":
            starting_functions = self.get_arg(2)
            self.if_food_ahead(starting_functions[0], starting_functions[1])
        elif self.func[0] == "prog2":
            starting_functions = self.get_arg(2)
            self.prog2(starting_functions[0], starting_functions[1])
        elif self.func[0] == "prog3":
            starting_functions = self.get_arg(3)
            self.prog3(starting_functions[0], starting_functions[1], starting_functions[2])
        elif self.func[0] == "move":
            self.move()
        elif self.func[0] == "left":
            self.left()
        elif self.func[0] == "right":
            self.right()

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
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.array = [[None for _ in range(width)] for _ in range(height)]
        self.add_food_specific_map(THE_GRID)
        #self.add_food_random(self.FOOD_NUM)
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
    
    def add_food_random(self, food_num):
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
        # build a specific map
        # given a string
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
    # print("grid created")

    # for i in range(50):
    #     a = Agent(grid)
    #     if "move" not in a.phenotype:
    #         continue

    # #a.phenotype = "if_food_ahead(move,if_food_ahead(left,prog2(move,left)))"

    #     print("the phenotype is ", a.phenotype)
    #     a.run_phenotype()
    #     grid.print_history(a)
    #     print("cost is ", a.gene.cost)
    #     print("_____________________")

    # ideal phenotype testing
#"if_food_ahead(move, prog2(left, if_food_ahead(move,prog3(right,right,if_food_ahead(move,prog3(move,left,move))))))"
    ideal = "if_food_ahead(move, prog2(left, if_food_ahead(move,prog3(right,right,if_food_ahead(move,prog3(move,left,move))))))"
    a = Agent(grid)
    a.phenotype = ideal
    a.run_phenotype()
    grid.print_history(a)
    