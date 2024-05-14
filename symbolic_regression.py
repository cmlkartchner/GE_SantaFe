import numpy as np
import random
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, init_printing
from deap import base, creator, tools, gp

init_printing() 

random.seed(45) # we set the seed to the same number so we don't need to set it each time

x = np.linspace(-10, 10, 200) # input data

true_relationship = lambda x: x**2 + 2*x + 1

'''
Now we need to generate the output
We will use noise values since we are working with synthetic data
Noise values basically means the variation use to simulate real world imperfections
'''

noise = np.random.normal(0, 120, x.shape) 
'''
    - 0 is the mean 
    - 10 is the standard deviation 
    - x.shape takes in account all input values for the size of the array
    - try: change standard deviation to test data plot
'''
print("Number of input values:", str(x.size))
y = true_relationship(x) + noise

# Symbolic expression: y = x^2 + 2x + 1
x_sym = symbols('x')
expression_sym = x_sym**2 + 2*x_sym + 1
print("Expression: y = " + str(expression_sym))

x_sym = symbols('x')
solutions = solve(Eq(expression_sym,0), x_sym)
print("Solutions for Y:", solutions)

# Plotting the data
plt.scatter(x, y, label = "noise")
plt.plot(x, true_relationship(x), color = 'red', label = 'True Rleationship')
plt.legend()
plt.show()

# TODO: implement GE to find mathematical models that fit the noise data
print("GE Section:")
rules = {
    # TODO: create rules
}
