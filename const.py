# production constrants
POPULATION_LIMIT = 100
GENE_LEN = 100
NEIGHBOOR_SIZE = 8

# evolve constants
GENERATIONS = 50

Base_DIVERSITY = .7
Base_FOOD_INCENTIVE = 1.1
Base_CONSECUTIVE_FOOD = .7
Base_OFFPATHPENALTY = .2
Base_DISTANCEPINCH = .05
Base_MUTATION_RATE = .9

DIVERSITY = 0
LEARNED_ACCP = .5
SELFTAUGHT_ACCP = .8
FOOD_INCENTIVE = 0
CONSECUTIVE_FOOD = 0
DISTANCEPINCH = 0
MUTATION_RATE = 0  
OFFPATHPENALTY = 0  

INCENTIVE_RATE_INCREASE = 1.1
PENALTY_RATE_INCREASE = 1.2

INCENTIVE_RATE_DECREASE = .90
PENALTY_RATE_DECREASE = .80

FITNESS_UPPER_THRESHOLD = 0.65
FITNESS_LOWER_THRESHOLD = 0.5

NUM_COMPETITORS = 5 # number of competitors used in tournament selection
SELECTION_PROPORTION = 0.3 # proportion of population selected for parents for crossover
NUM_MOVES = 400 # number of actions an agent can perform before simulation is ended
TOURNAMENT_SIZE = 5
POP_SIZE = 3 # number of parents to return from NSGA-II selection

# Grid constrants
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


RULES = {
        "<code>": ["<code>", "<progs>"],
        "<progs>": ["<condition>","<prog2>","<prog3>","<op>"],
        "<condition>" : ["if_food_ahead(<progs>,<progs>)"],
        "<prog2>" : ["prog2(<progs>,<progs>)"],
        "<prog3>" : ["prog3(<progs>,<progs>,<progs>)"],
        "<op>" :["left","right","move"] 
    }

# agent constants
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
NUM_AGENTS = 100
DIVERSITY_CONSTANT = 4 # controls how much diversity affects fitness (lower = more effect)
DIVERSITY_REWARD = 2 # fixed reward for diversity (a 2nd implementation of diversity)

# grid constants
GRID_WIDTH = 32
GRID_HEIGHT = 32
FOOD_NUM = 89