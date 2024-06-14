import random
import numpy as np
from gene import Gene
import constants as constants
from copy import deepcopy
from grid_and_food import Grid, Food
from hiveMind import EndException

class Agent:
    def __init__(self, grid, id='', gene=None) -> None:
        self.Gene = Gene(np.random.randint(101, size=constants.GENE_LEN))
        self.neighboorGeneList = []
        self.id = id
        # cost information
        self.food_touched = 0 # (no food should be double counted)
        self.distance = 0 # how far it has traveled (distance not displacement)
        self.moves = 0 # how many actions: left, right, move

        # agent id: either set manually else set randomly
        if id is None:
            self.id = random.randint(0, 1000000)
        else:
            self.id = id

        self.heading = constants.NORTH
        self.position = (0,0) # currently we have every agent starting at the same location
        #self.position = (random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT))
        
        self.grid = grid # every agent is using the SAME grid object
        self.grid.update_history(self, self.position) # init with starting position

        self.memory = [] # list to contain the gene objects of neighbors

        # gene: can either be inserted manually (for 'testing' genes during act function), else set randomly
        if gene is None:
            self.gene = Gene([random.randint(0, 100) for i in range(constants.GENE_LEN)])
        else:
            self.gene = deepcopy(gene)
            
        # generate string representation of program from grammar
        self.phenotype = self.gene.generate_phenotype(constants.RULES, "<code>") 

        self.index = 0 # index of self.func
        self.func = None # parsed list of functions representing the current phenotype
        self.terminal_functions_run = 0
    
    def printID(self):
        print(f"{self.id}ID")
        
    def printGene(self):
        print(self.Gene.genotype)
    
    def printNeighboors(self):
        print(self.neighboorGeneList)

    # functions for running the phenotype once it has been generated and parsed by get_args
    def prog2(self, progs1, progs2):
        progs1()
        progs2()

    def prog3(self, progs1, progs2, progs3):
        progs1()
        progs2()
        progs3()

    def food_ahead(self):
        # check if there is food in front of the agent
        if self.heading == constants.NORTH:
            return self.grid.in_bounds(self.position[0],self.position[1] - 1) and isinstance(self.grid.array[self.position[1]-1][self.position[0]], Food)
        elif self.heading == constants.EAST:
            return self.grid.in_bounds(self.position[0] + 1,self.position[1]) and isinstance(self.grid.array[self.position[1]][self.position[0] + 1], Food)
        elif self.heading == constants.SOUTH:
            return self.grid.in_bounds(self.position[0],self.position[1] + 1) and isinstance(self.grid.array[self.position[1] + 1][self.position[0]], Food)
        elif self.heading == constants.WEST:
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

        if self.heading == constants.NORTH:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.heading == constants.EAST:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.heading == constants.SOUTH:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.heading == constants.WEST:
            self.position = (self.position[0] - 1, self.position[1])
        else:
            print("Error: heading not found")
            return
        
        # circular grid with no end
        if self.position[0] >= constants.GRID_WIDTH:
            self.position = (0, self.position[1])
        elif self.position[0] == -1:
            self.position = (constants.GRID_WIDTH - 1, self.position[1])
        
        if self.position[1] >= constants.GRID_HEIGHT:
            self.position = (self.position[0], 0)
        elif self.position[1] == -1:
            self.position = (self.position[0], constants.GRID_HEIGHT - 1)

        # avoid double counting food (note: the grid is never edited, nor is the agent ever inserted into it.
        # The agent just tracks its location in self.grid.history dictionary)
        if isinstance(self.grid.array[self.position[1]][self.position[0]], Food) and self.position not in self.grid.history[self.id]:
            self.food_touched += 1
        self.grid.update_history(self, self.position)
        self.distance += 1

    def if_food_ahead(self, arg1, arg2):
        if self.food_ahead():
            arg1()
        else:
            arg2()
    
    # IMPORTANT ADDITION TO FIX WEIRD LAMBDA ERRORS
    def append_lambda(self, args, arguments, type): 
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
    
    # functions to taking the output of generate_phenotype and turning it into a runnable program
    def run_phenotype_once(self): # master function (calls all the other functions in this section)
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
    
    def run_phenotype(self, population):
        # repeatedly run the phenotype until the should_end is true
        try:
            self.grid.history[self.id] = set() # reset before running again
            self.moves = 0
            self.food_touched = 0
            self.distance = 0
            self.terminal_functions_run = 0
            self.position = (0,0)
            #self.position = (random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT))
            while(True):
                self.run_phenotype_once()
        except EndException as e:
            # reward for food, punish for distance
            self.gene.cost = self.food_touched - (self.distance * .05)
            if self.food_touched == constants.FOOD_NUM: # anyone who gets them all gets big reward
                self.gene.cost += 50
            #TODO: how big should the diversity addition be? 
            #print("cost: ", self.phenotype, "\n->", self.gene.cost)
    
    # functions for ending the simulation (terminal_functions_run is probably useless)
    def should_end(self):
        self.terminal_functions_run += 1
        if self.food_touched == constants.FOOD_NUM or self.moves == constants.NUM_MOVES or self.terminal_functions_run == 1000:
            return True
        return False
    
    def end(self):
        raise EndException("End of simulation")
    
    def sense(self, neighboors, hiveMind):
        self.neighboorList.clear()
        for num in neighboors:
            self.neighboorGeneList.append(hiveMind.agentList[num].Gene.genotype)

if __name__ == "__main__":
    grid = Grid(constants.GRID_WIDTH, constants.GRID_HEIGHT)
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