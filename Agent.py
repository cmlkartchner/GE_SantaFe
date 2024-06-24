import random
from Gene import Gene
import const as const
from copy import deepcopy
from Grid_Food_EndExpect import Grid, Food, EndException
from GGraph_Node import GGraph

class Agent:
    def __init__(self, grid, id='', gene=None) -> None:
        if gene is None:
            self.gene = Gene([random.randint(0, 100) for x in range(const.GENE_LEN)])
        else:
            self.gene = deepcopy(gene)
            
        # cost information
        self.food_touched = 0 # (no food should be double counted)
        self.distance = 0 # how far it has traveled (distance not displacement)
        self.moves = 0 # how many actions: left, right, move

        # agent id: either set manually else set randomly
        if id == '':
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id

        self.heading = const.NORTH
        self.position = (0,0) # currently we have every agent starting at the same location
        #self.position = (random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT))
        
        self.grid = grid # every agent is using the SAME grid object
        self.grid.update_history(self, self.position) # init with starting position

        self.memory = [] 
            
        # generate string representation of program from grammar
        self.phenotype = self.gene.generate_phenotype(GGraph(const.RULES), "<code>") 

        self.index = 0 # index of self.func
        self.func = None # parsed list of functions representing the current phenotype
        self.terminal_functions_run = 0
    
    def printID(self):
        print(f"{self.id}ID")

    # moving fuctions
    def food_ahead(self):
        # check if there is food in front of the agent
        if self.heading == const.NORTH:
            return self.grid.in_bounds(self.position[0],self.position[1] - 1) and isinstance(self.grid.array[self.position[1]-1][self.position[0]], Food)
        elif self.heading == const.EAST:
            return self.grid.in_bounds(self.position[0] + 1,self.position[1]) and isinstance(self.grid.array[self.position[1]][self.position[0] + 1], Food)
        elif self.heading == const.SOUTH:
            return self.grid.in_bounds(self.position[0],self.position[1] + 1) and isinstance(self.grid.array[self.position[1] + 1][self.position[0]], Food)
        elif self.heading == const.WEST:
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

        if self.heading == const.NORTH:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.heading == const.EAST:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.heading == const.SOUTH:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.heading == const.WEST:
            self.position = (self.position[0] - 1, self.position[1])
        else:
            print("Error: heading not found")
            return
        
        # circular grid with no end
        if self.position[0] >= const.GRID_WIDTH:
            self.position = (0, self.position[1])
        elif self.position[0] == -1:
            self.position = (const.GRID_WIDTH - 1, self.position[1])
        
        if self.position[1] >= const.GRID_HEIGHT:
            self.position = (self.position[0], 0)
        elif self.position[1] == -1:
            self.position = (self.position[0], const.GRID_HEIGHT - 1)

        # avoid double counting food (note: the grid is never edited, nor is the agent ever inserted into it.
        # The agent just tracks its location in self.grid.history dictionary)
        if isinstance(self.grid.array[self.position[1]][self.position[0]], Food) and self.position not in self.grid.history[self.id]:
            self.food_touched += 1
        self.grid.update_history(self, self.position)
        self.distance += 1

    # functions for running the phenotype once it has been generated and parsed by get_args
    def if_food_ahead(self, arg1, arg2):
        if self.food_ahead():
            arg1()
        else:
            arg2()
    
    def prog2(self, progs1, progs2):
        progs1()
        progs2()

    def prog3(self, progs1, progs2, progs3):
        progs1()
        progs2()
        progs3()
        
    def append_lambda(self, args, arguments, type): 
        # store the nested lambda functions
        arg1, arg2 = arguments[0], arguments[1]
        if type == "if_food_ahead":
            args.append(lambda: self.if_food_ahead(arg1, arg2))
        elif type == "prog2":
            args.append(lambda: self.prog2(arg1, arg2))
        elif type == "prog3":
            arg3 = arguments[2]
            args.append(lambda: self.prog3(arg1, arg2, arg3))
    
    # returns a list of lambda functions
    def get_arg(self, num_args): 
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
                self.index += 1
                arguments = self.get_arg(2)
                self.append_lambda(args, arguments, "if_food_ahead")
            elif self.func[self.index] == "prog2":
                self.index += 1
                arguments = self.get_arg(2)
                self.append_lambda(args, arguments, "prog2")
            elif self.func[self.index] == "prog3":
                self.index += 1
                arguments = self.get_arg(3)
                self.append_lambda(args, arguments, "prog3")
            else:
                print("Error: function not found")
            num_args -= 1
        return args
    
    # parse the phenotype into a list of functions to call get_args on
    def parse_phenotype(self):
        self.func = self.phenotype.replace("(", " ").replace(")", " ").replace(",", " ").split()
    
    # functions to taking the output of generate_phenotype and turning it into a runnable program
    def run_phenotype_once(self):
        self.parse_phenotype()
        # skip the first function becasue it is processed here
        self.index = 1 

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
    
    def run_phenotype(self):
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
        except EndException:
            # reward for food, punish for distance
            self.gene.cost = self.food_touched - (self.distance * .05)
            if self.food_touched == const.FOOD_NUM:
                self.gene.cost += 50
            #TODO: how big should the diversity addition be? 
            #print("cost: ", self.phenotype, "\n->", self.gene.cost)
    
    # functions for ending the simulation (terminal_functions_run is probably useless)
    def should_end(self):
        self.terminal_functions_run += 1
        if self.food_touched == const.FOOD_NUM or self.moves == const.NUM_MOVES or self.terminal_functions_run == 1000:
            return True
        return False
    
    def end(self):
        raise EndException("End of simulation")
    
    def sense(self, neighboors):
        self.memory.clear()
        self.memory.extend(neighboors)
    
    def parentSelection(self):
        parents = []
        for agent in self.memory:
            if agent.gene.cost >= self.gene.cost:
                parents.append(agent)
        return parents        
        
    def actUpdate(self):
        parentAgents = self.parentSelection()
        childrenGenes = self.gene.crossoverProduction(parentAgents)
        agents = []
        for gene in childrenGenes:
            grid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT)
            gene.mutate()
            a = Agent(grid, gene=gene)
            agents.append(a)
            a.run_phenotype()
        for agent in agents:
            if agent.gene.cost > self.gene.cost:
                self.gene = agent.gene

if __name__ == "__main__":
    for i in range(10):
        grid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT) 
        a = Agent(grid)
        if "move" not in a.phenotype:
            continue
        a.run_phenotype()
        # if a.gene.cost > 10:
        print("the phenotype is ", a.phenotype)
        grid.print_history(a)
        print("cost is ", a.gene.cost)
        print("_____________________")