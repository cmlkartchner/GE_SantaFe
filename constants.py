GENE_LEN = 100 # length of the genotype
RULES = {
        "<code>": ["<code>", "<progs>", "<progs>"],
        "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
        "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
        "<prog2>" : ["prog2(<progs>,<progs>)"],
        "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
        "<op>" :["left","right","move"] 
    }

# evolve constants
POPULATION_SIZE = 50

# agent constants
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# grid constants
GRID_SIZE = 10