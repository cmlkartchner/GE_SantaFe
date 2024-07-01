GENE_LEN = 500 # length of the genotype
RULES = {
        "<code>": ["<code>", "<progs>",],
        "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
        "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
        "<prog2>" : ["prog2(<progs>,<progs>)"],
        "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
        "<op>" :["left","right","move"] 
    }

# evolve constants
GENERATIONS = 500
NUM_COMPETITORS = 5 # number of competitors used in tournament selection
SELECTION_PROPORTION = 0.3 # proportion of population selected for parents for crossover
NUM_STEPS = 650 # number of actions an agent can perform before simulation is ended
TOURNAMENT_SIZE = 5
POP_SIZE = 3 # number of parents to return from NSGA-II selection

# agent constants
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
NUM_AGENTS = 50
DIVERSITY_CONSTANT = 5 # controls how much diversity affects fitness (lower = more effect)
DIVERSITY_REWARD = 5 # fixed reward for diversity (a 2nd implementation of diversity)

# grid constants
GRID_WIDTH = 32
GRID_HEIGHT = 32
FOOD_NUM = 89

THE_GRID = """
    .###............................
    ...#............................
    ...#.....................###....
    ...#....................#....#..
    ...#....................#....#..
    ...####.#####........##.........
    ............#................#..
    ............#.......#...........
    ............#.......#........#..
    ............#.......#...........
    ....................#...........
    ............#................#..
    ............#...................
    ............#.......#.....###...
    ............#.......#..#........
    .................#..............
    ................................
    ............#...........#.......
    ............#...#..........#....
    ............#...#...............
    ............#...#...............
    ............#...#.........#.....
    ............#..........#........
    ............#...................
    ...##. .#####....#..............
    .#..............#...............
    .#..............#...............
    .#......#######.................
    .#.....#........................
    .......#........................
    ..####..........................
    ................................"""


# TODO: figure out which constants are relevant
# CODON_SIZE:             100
# CROSSOVER:              variable_onepoint
# CROSSOVER_PROBABILITY:  0.9
# GENERATIONS:	        1
# MAX_GENOME_LENGTH:      500
# GRAMMAR_FILE:           ..,santa_fe_trail.bnf
# INITIALISATION:         PI_grow
# INVALID_SELECTION:      True
# MAX_INIT_TREE_DEPTH:    12
# MAX_TREE_DEPTH:         16
# MUTATION:               int_flip_per_codon
# POPULATION_SIZE:	    100
# FITNESS_FUNCTION:       santa_fe_trail.santa_fe_trail
# REPLACEMENT:            generational
# SELECTION:              truncation
# SELECTION_PROPORTION:   0.4
# TOURNAMENT_SIZE:        4
# MUTATION_PROBABILITY:   0.75

# generation 58  highest cost is  545.0
# most food gotten:  58

# generation 14  highest cost is  554.0
# most food gotten:  58
# steps taken:  104
# SELECTION_PROP:   0.4
# TOURNAMENT:        4
# MUTATION_PROB:   0.75
# POPULATION:	    100