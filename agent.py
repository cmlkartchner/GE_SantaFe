from ge_utils import Gene
import random
from constants import GENE_LEN, GRID_HEIGHT, GRID_WIDTH, RULES, THE_GRID, FOOD_NUM
from constants import NORTH, EAST, SOUTH, WEST
from end_exception import EndException

class Agent:
    def __init__(self, grid) -> None:
        # cost information
        self.food_touched = 0 # no duplicates
        self.distance = 0 # how far it has traveled (not displacement)
        self.moves = 0 # how many actions: left, right, move

        # simulation information
        self.id = random.randint(0, 1000000)
        self.heading = NORTH
        self.position = (random.randint(0,GRID_WIDTH), random.randint(0,GRID_HEIGHT)) # x,y BUT in the grid it is y,x
        self.grid = grid
        
        self.grid.update_history(self, self.position) # init with starting position

        # genetic information
        self.memory = [] # contains multiple genes
        self.gene = Gene([random.randint(0, 100) for i in range(GENE_LEN)])
        self.phenotype = self.gene.generate_phenotype(RULES, "<code>")

        self.index = 0

    # functions from the grammar
    def prog2(self, progs1, progs2):
        print("prog2 with arguments", progs1, progs2)
        # if callable(progs1): # case where prog2 was INSIDE a if_food_ahead
        #     progs1()
        # if callable(progs2):
        #     progs2()
    def prog3(self, progs1, progs2, progs3):
        print("prog3 with arguments", progs1, progs2, progs3)
        # if callable(progs1): # case where prog3 was INSIDE a if_food_ahead (which cannot have function calls)
        #     progs1()
        # if callable(progs2):
        #     progs2()
        # if callable(progs3):
        #     progs3()

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
        print("lEft")
        # if self.should_end():
        #     self.end()
        # self.moves+=1
        # self.heading = (self.heading - 1) % 4
    def right(self):
        print("right")
        # if self.should_end():
        #     self.end()
        # self.moves+=1
        # self.heading = (self.heading + 1) % 4
    def move(self):
        print("MOVE")
        # if self.should_end():
        #     self.end()
        # self.moves+=1
        # prev_position = self.position
        # if self.heading == NORTH and self.grid.in_bounds(self.position[0],self.position[1] - 1):
        #     self.position = (self.position[0], self.position[1] - 1)
        # elif self.heading == EAST and self.grid.in_bounds(self.position[0] + 1,self.position[1]):
        #     self.position = (self.position[0] + 1, self.position[1])
        # elif self.heading == SOUTH and self.grid.in_bounds(self.position[0],self.position[1] + 1):
        #     self.position = (self.position[0], self.position[1] + 1)
        # elif self.heading == WEST and self.grid.in_bounds(self.position[0] - 1,self.position[1]):
        #     self.position = (self.position[0] - 1, self.position[1])
        # else: # did not move
        #     return
        
        # # avoid double counting food
        # if isinstance(self.grid.array[self.position[1]][self.position[0]], Food) and self.position not in self.grid.history[self.id]:
        #     self.food_touched += 1
        # self.grid.update_history(self, self.position)
        # self.distance += 1





    def if_food_ahead(self, arg1, arg2):

        # if_food_ahead(if_food_ahead(move,move),if_food_ahead(left,prog2(move,move)))
        print("if food ahead with arguments")
        # if self.food_ahead() and callable(arg1):
        #     arg1()
        # elif callable(arg2):
        #     arg2()
        
        #print(arg2)
        # if the one is not callable then that means it was already called and evaluted to none
        # so no need to do anything extra
        # example case: if_food_ahead(left,prog2(move,move))

    # functions for ending the simulation
    def should_end(self):
        if self.food_touched == FOOD_NUM or self.moves == 400:
            return True
        return False
    def end(self):
        raise EndException("End of simulation")
    


    def get_arg(self, num_args): # returns a list of lambda functions
        # starting at index
        prog3 = self.prog3
        prog2 = self.prog2
        left = self.left
        right = self.right
        move = self.move
        if_food_ahead = self.if_food_ahead

        move = lambda: move()
        left = lambda: left()
        right = lambda: right()

        #num_args = 2 # imagine we reached a if_food ahead and the first arg is if_food_ahead
        #woops it is using the wrong index....num_args 

        func = ["if_food_ahead", "move", "prog2", "left", "right", "prog3", "if_food_ahead", "move", "left", "right", "right"]
        args = [] # holds num_args lambda functions
        while num_args > 0:
            if func[self.index] in ["move", "left", "right"]:
                if func[self.index] == "move":
                    args.append("lambda : move()")
                    #args.append(move)
                elif func[self.index] == "left":
                    args.append("lambda : left()")
                    #args.append(left)
                elif func[self.index] == "right":
                    args.append("lambda : right()")
                    #args.append(right)
                self.index+=1

            elif func[self.index] == "if_food_ahead":
                self.index+=1
                # goal: 2 lambda functions to pass in
                arguments = self.get_arg(2)
                #print(arguments)
                #print("lambda: if_food_ahead(", arguments[0], arguments[1], ")")
                args.append(f"lambda : if_food_ahead({arguments[0]}, {arguments[1]})")
                #args.append(lambda : if_food_ahead(arguments[0], arguments[1]))

            elif func[self.index] == "prog2":
                self.index+=1
                # goal: 2 lambda functions to pass in

                arguments = self.get_arg(2)
                args.append(f"lambda : prog2({arguments[0]}, {arguments[1]})")
            
            elif func[self.index] == "prog3":
                self.index+=1
                # goal: 3 lambda functions to pass in
                
                arguments = self.get_arg(3)
                #print(arguments)
                #print("lambda: prog3(", arguments[0], arguments[1], arguments[2], ")")
                #args.append(lambda : prog3(arguments[0], arguments[1], arguments[2]))
                args.append(f"lambda : prog3({arguments[0]}, {arguments[1]})")
            
            else:
                print("Error: function not found")
            
            num_args -= 1
        
        return args
                
    def run_phenotype(self, phenotype):
        # TODO: 
        prog3 = self.prog3
        prog2 = self.prog2
        left = self.left
        right = self.right
        move = self.move
        if_food_ahead = self.if_food_ahead


        
    
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
    print("grid created")

    a = Agent(grid)
    grid.print_grid()
    a.phenotype = "if_food_ahead(move,if_food_ahead(left,prog2(move,left)))"
    # a.run_phenotype(a.phenotype)
    
    #"prog3(if_food_ahead(left,right),right,prog3(prog2(move,prog2(right,move)),left,right))"
    #"prog3(move, prog2(move, if_food_ahead(right,left)),move)"
    #print(a.get_arg(0, 2))
    functions = a.get_arg(2)
    #eval(a.get_arg(0, 2))
    print(functions)
    # for func in functions:
    #     func()

