import numpy as np
import random
from sympy import symbols, Eq, solve, init_printing

random.seed(45) # we set the seed to the same number so we don't need to set it each time

x = np.linspace(-10, 10, 200) # setting values for x - input data

true_relationship = lambda x: x**2 + 2*x + 1 # this is the equation to solve for y - lambda x = y

'''
now we need to generate the output
we will use noise values since we are working with synthetic data
noise values basically means the variation use to simulate real world imperfections
'''

noise = np.random.normal(0, 10, x.shape) 
'''
    - 0 is the mean 
    - 10 is the standard deviation 
    - x.shape takes in account all inputs for the size of the array
'''
y = true_relationship(x) + noise

# y = x^2 + 2x + 1
init_printing() 
expression = x**2 + 2*x + 1
print("Expression:" + str(expression))