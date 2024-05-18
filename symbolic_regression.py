import operator
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from sympy import symbols, Eq, solve, init_printing
from deap import base, creator, tools, gp, algorithms

def safe_div(num, den):
    if den == 0:
        return 1
    else:
        return num / den

def rand101():
    return random.randint(-10, 10)

init_printing()

random.seed(45)

x = np.linspace(-10, 10, 200)
true_relationship = lambda x: x**2 + 2*x + 1
'''
    - 0 is the mean 
    - 10 is the standard deviation 
    - x.shape takes in account all input values for the size of the array
    - try: change standard deviation to test data plot
'''
noise = np.random.normal(0, 120, x.shape)
y = true_relationship(x) + noise

print("Number of input values:", x.size)
x_sym = symbols('x')
expression_sym = x_sym**2 + 2*x_sym + 1 # symbolic expression
print("Expression: y =", expression_sym)

solutions = solve(Eq(expression_sym, 0), x_sym)
print("Solutions for y = 0:", solutions)

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addEphemeralConstant("rand101", partial(rand101))
pset.renameArguments(ARG0 = 'x')

creator.create("FitnessMin", base.Fitness, weights = (-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness = creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset = pset, min_= 1, max_ = 3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset = pset)

def eval_genetic_expression(individual):
    func = toolbox.compile(expr = individual)
    try:
        predictions = np.array([func(xi) for xi in x])
        mse = ((y - predictions) ** 2).mean()
    except Exception as e:
        mse = np.inf
    return (mse,)

toolbox.register("evaluate", eval_genetic_expression)
toolbox.register("select", tools.selTournament, tournsize = 3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutUniform, expr = toolbox.expr, pset = pset)
toolbox.decorate("mate", gp.staticLimit(key = operator.attrgetter("height"), max_value = 17))
toolbox.decorate("mutate", gp.staticLimit(key = operator.attrgetter("height"), max_value = 17)) 

def main():
    pop = toolbox.population(n = 300)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats = stats, halloffame = hof, verbose = True)

    return pop, stats, hof

if __name__ == "__main__":
    final_pop, stats, hof = main()
    best_func = toolbox.compile(expr = hof[0])
    predictions = [best_func(xi) for xi in x]

    '''
        Now we need to generate the output
        We will use noise values since we are working with synthetic data
        Noise values basically means the variation use to simulate real world imperfections
    '''

    plt.scatter(x, y, color = 'red', label = 'Noisy Data')
    plt.plot(x, true_relationship(x), label = 'True Relationship')
    plt.plot(x, predictions, label = 'Evolved Model')
    plt.title("Comparison of True Relationship and Evolved Model")
    plt.legend()
    plt.show()
    print("Best individual is:", hof[0], "with fitness:", hof[0].fitness)