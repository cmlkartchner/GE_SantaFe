from ge_utils import Gene, GENE_LEN, generate_phenotype # GENE_LEN in paper is 100

from enum import Enum
import random

santa_fe_rules = {
    "<code>": ["<code>", "<progs>"],
    "<progs>": ["<condition>", "<prog2>", "<prog3>", "<op>"],
    "<condition>": ["if_food_ahead(<progs>,<progs>)"],
    "<prog2>": ["prog2(<progs>,<progs>)"],
    "<prog3>": ["prog3(<progs>,<progs>,<progs>)"],
    "<op>": ["left", "right", "move"]
}

Direction = Enum('Direction', ['NORTH', 'SOUTH', 'EAST', 'WEST'])

WORLD_SIZE = 5 # paper is 32
NUM_AGENTS = 10 # paper had 100 agents
INTERACT_PROB = 0.85
TOURNAMENT_SIZE = 5
POP_SIZE = 3
CROSSOVER_PROB = 0.9
MUTATION_PROB = 0.01

### CLASSES ###
class SantaFe_World:
    def __init__(self):
        self.trail = self.load_trail()

    # x and y are flipped
    def load_trail(self):
        trail_file = 'santafe/test_trail.txt'
        trail = list()
        with open(trail_file, "r") as file:
            for i, line in enumerate(file):
                trail.append(list())
                for j, col in enumerate(line):
                    if col == "#":
                        trail[-1].append("food")
                    elif col == ".":
                        trail[-1].append("empty")
                    elif col == "S":
                        trail[-1].append("empty")
                        self.trail_start = [i, j]
        return trail

    def get_trail_info(self, x, y):
        return self.trail[x][y]

class SantaFe_Agent:
    def __init__(self, heading, pos=[0, 0], world=None, sim=None, gene=None, id=0):
        self.heading = heading
        self.pos = pos
        self.world = world
        self.sim = sim
        self.gene = gene
        self.neighbors = None
        self.num_food_eaten = 0
        self.trail_food_eaten = [[0 for j in range(WORLD_SIZE)] for i in range(WORLD_SIZE)]
        self.id = id

    ### GRAMMAR TERMINALS ###
    def left(self):
        # given a heading, turn the heading left
        match self.heading:
            case Direction.NORTH:
                self.heading = Direction.WEST
            case Direction.SOUTH:
                self.heading = Direction.EAST
            case Direction.EAST:
                self.heading = Direction.NORTH
            case Direction.WEST:
                self.heading = Direction.SOUTH

    def right(self):
        # given a heading, turn the heading right
        match self.heading:
            case Direction.NORTH:
                self.heading = Direction.EAST
            case Direction.SOUTH:
                self.heading = Direction.WEST
            case Direction.EAST:
                self.heading = Direction.SOUTH
            case Direction.WEST:
                self.heading = Direction.NORTH

    def move(self):
        # given a heading, move forward one space in that heading's direction
        # print(self.heading)
        # print(self.pos)
        # print("Move forward")
        match self.heading:
            case Direction.NORTH:
                self.pos[1] = (self.y() - 1) % WORLD_SIZE
            case Direction.SOUTH:
                self.pos[1] = (self.y() + 1) % WORLD_SIZE
            case Direction.EAST:
                self.pos[0] = (self.x() - 1) % WORLD_SIZE
            case Direction.WEST:
                self.pos[0] = (self.x() + 1) % WORLD_SIZE

        if self.world.get_trail_info(self.y(), self.x()) == "food":
            self.num_food_eaten += 1
            self.mark_trail()

    def if_food_ahead(self, if_true, if_false):
        if self.sense_food():
            if_true()
        else:
            if_false()

    ### GEESE ALGORITHM FUNCTIONS ###
    def sense(self):
        # SENSE: get agent neighbors' genotypes
        self.neighbors = self.sim.get_neighbors(self)

    def act(self):
    # ACT: add own genotype to pool of collected genotypes
        if self.neighbors:
            self.neighbors.append(self)
            # select fit genotypes using tournament method; fitness is implicit in each neighbor's "num_food_eaten"
            parents = tournament_select(self.neighbors)
            # perform crossover on selected genotypes
            child_gene1, child_gene2 = crossover(self.sim.get_agent_gene(parents[0].id), self.sim.get_agent_gene(parents[1].id)) # TODO: make this dynamic to fit POP_SIZE
            # mutate children
            mutate(child_gene1, child_gene2)
            # evaluate children
            eval_fitness(SantaFe_Agent(random.choice(list(Direction)), random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1),
                                       self.sim, child_gene1))
            # return most fit child

    def update(self):
        # UPDATE: if new genotype from act() is better than current genotype,
        #         replace current genotype with new genotype
        pass

    ### AGENT UTILS ###
    def sense_food(self):
        # return whether or not there is food ahead of the agent
        match self.heading:
            case Direction.NORTH:
                if self.world.get_trail_info((self.y()-1) % WORLD_SIZE, self.x()) == "food":
                    return True
            case Direction.SOUTH:
                if self.world.get_trail_info((self.y()+1) % WORLD_SIZE, self.x()) == "food":
                    return True
            case Direction.EAST:
                if self.world.get_trail_info((self.y(), self.x()-1) % WORLD_SIZE) == "food":
                    return True
            case Direction.WEST:
                if self.world.get_trail_info(self.y(), (self.x()+1) % WORLD_SIZE) == "food":
                    return True
        print("No food ahead")
        return False

    def do_routine(self, routine): # double functions as fitness function
        left = self.left
        right = self.right
        move = self.move
        if_food_ahead = self.if_food_ahead

        # add parentheses to all the left right move calls that are not nested within if_food_ahead
        # first, have placeholder characters
        routine = routine.replace("left", "left||").replace("right", "right||").replace("move", "move||")
        for i in range(len(routine)):
            if routine[i:].startswith("if_food_ahead"):
                left_index = routine.find("(", i)
                right_index = routine.find(")", i)
                fixed_string = routine[left_index:right_index].replace("|", "")
                routine = routine[:left_index] + fixed_string + routine[right_index:]
        routine = routine.replace("||", "()")
        try:
            eval(routine)
        except SyntaxError: # TODO: check what error it would actually throw
            print("Invalid routine")
            self.num_food_eaten = -1

    def mark_trail(self):
        self.trail_food_eaten[self.x()][self.y()] = 1 # TODO: Double check that it's marking the place you want it to

    def x(self):
        return self.pos[0]
    
    def y(self):
        return self.pos[1]

class SantaFe_Sim:
    def __init__(self, world=None) -> None:
        self.world = world
        self.prev_state = dict()
        self.agents = self.build_agents()

    def build_agents(self):
        agents = []
        for i in range(NUM_AGENTS):
            direction = random.choice(list(Direction))
            pos = [random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)]
            gene = Gene(random.sample(range(1,1000), GENE_LEN))
            agents.append(SantaFe_Agent(direction, pos, self.world, self, gene, i))
            self.prev_state.update({i: gene})
        return agents
    
    def get_neighbors(self, agent):
        neighbors = []
        for neighbor in self.agents:
            if agent is not neighbor:
                if random.random() < INTERACT_PROB:
                    neighbors.append(neighbor)
        return neighbors
    
    def get_agent_gene(self, agent_id):
        return self.prev_state.get(agent_id)

    def run_iter(self):
        for agent in self.agents:
            agent.num_food_eaten = 0 # reset from last evaluation
            eval_fitness(agent)

            agent.sense()
            agent.act()
            agent.update()

### GA HELPER FUNCTIONS ###
def eval_fitness(agent):
    routine = generate_phenotype(santa_fe_rules, "<code>", agent.gene)
    agent.gene.phenotype = routine

    if "<" in routine or "ERROR" in routine:
        agent.num_food_eaten = -1
    else:
        agent.do_routine(routine)

# assumes eval_fitness was called for each agent
def tournament_select(agents):
    winners = []
    for i in range(POP_SIZE):
        participants = random.sample(agents, TOURNAMENT_SIZE)
        most_fit_agent = participants[0]
        # select most fit individuals from tournament
        for agent in participants:
            if agent.num_food_eaten > most_fit_agent.num_food_eaten:
                most_fit_agent = agent
        winners.append(most_fit_agent)
    return winners

def crossover(parent_gene1: Gene, parent_gene2: Gene):
    if random.random() < CROSSOVER_PROB:
        crossover_point = random.randint(1, min(len(parent_gene1.genotype), len(parent_gene2.genotype)) - 2)
        print(f"DEBUG Crossover index: {crossover_point}")
        child_gene1 = parent_gene1.genotype[:crossover_point] + parent_gene2.genotype[crossover_point:]
        child_gene2 = parent_gene2.genotype[:crossover_point] + parent_gene1.genotype[crossover_point:]
    else:
        child_gene1 = parent_gene1.genotype
        child_gene2 = parent_gene2.genotype

    return Gene(child_gene1), Gene(child_gene2)

def mutate(gene: Gene):
    for i in range(len(gene.genotype)):
        if random.random() < MUTATION_PROB:
            gene.genotype[i] = random.randint(0, 1000)
            print("DEBUG: gene mutated")
            return

### ADDITIONAL TERMINALS/UTILS ###
def prog2(prog_1, prog_2):
    progn(prog_1, prog_2)

def prog3(prog_1, prog_2, prog_3):
    progn(prog_1, prog_2, prog_3)

def progn(*args):
    for arg in args:
        if arg is not None:
            arg()

### TESTING ###


