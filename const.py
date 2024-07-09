# production constrants
POPULATION_LIMIT = 100
GENE_LEN = 200
NEIGHBOOR_SIZE = 4

# evolve constants
GENERATIONS = 150

Base_DIVERSITY = .6
Base_FOOD_INCENTIVE = 1.75
Base_CONSECUTIVE_FOOD = .25
Base_OFFPATHPENALTY = 0.05
Base_DISTANCEPINCH = 0
Base_MUTATION_RATE = .9

DIVERSITY = 0
LEARNED_ACCP = .7
SELFTAUGHT_ACCP = .7
FOOD_INCENTIVE = 0
CONSECUTIVE_FOOD = 0
DISTANCEPINCH = 0
MUTATION_RATE = 0  
OFFPATHPENALTY = 0

INCENTIVE_RATE_INCREASE = 1.05
PENALTY_RATE_INCREASE = 1.05

INCENTIVE_RATE_DECREASE = .95
PENALTY_RATE_DECREASE = .95

CONSEC_RATE_INCREASE = 1.1
CONSEC_RATE_DECREASE = .9

FITNESS_PEN_UPPER_THRESHOLD = 0.7
FITNESS_PEN_LOWER_THRESHOLD = 0.3

FITNESS_FOOD_UPPER_THRESHOLD = 0.8
FITNESS_FOOD_LOWER_THRESHOLD = 0.7

POPULATION_TOLERANCE = .75

CROSSOVER_PRODUCTION = 2
NOVELTY_TOLERANCE = .25

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
    ...##...#####....#..............
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