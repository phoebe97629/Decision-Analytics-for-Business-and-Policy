#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np
import csv
import os

# Demand in thousands of units
demand = np.array([15, 18, 14, 20])

# Plant capacity in thousands of units
capacity = np.array([20, 22, 17, 19, 18])

# Transportation costs per thousand units
# Hard coding the numbers for demonstration.
#transportCosts = np.array([[4000, 2500, 1200, 2200],
#              [2000, 2600, 1800, 2600],
#              [3000, 3400, 2600, 3100],
#              [2500, 3000, 4100, 3700],
#              [4500, 4000, 3000, 3200]])

# Alternatively, read 2D array from file
path = 'transportationCost.csv' # change to your file directory
data = np.genfromtxt(path, dtype=str, delimiter=',', encoding='utf-8-sig')
transportCosts = data.astype(np.float)
print transportCosts

# Indices for plants and markets
plants = range(len(capacity)) # Equivalently, plants = [0,1,2,3,4]
markets = range(len(demand)) # Equivalently, markets = [0,1,2,3]

# Setting up model object
m = Model()

### Setting up Decision Variables ###

# Transportation decision variables: x[i,j] captures the
# quantity to transport to market j from plant i

# Option 1: Define variables and objective at the same time
#x = m.addVars(plants, markets, obj=transportCosts, lb = 0.0)
#m.modelSense = GRB.MINIMIZE

# Option 2: Define variables, variable bounds, and objective separately
x = m.addVars(plants, markets)
m.setObjective(sum(sum(transportCosts[i,j] * x[i,j] for i in plants) for j in markets))
for i in plants:
    for j in markets:
        m.addConstr(x[i,j] >= 0.0)


### Constraints ###

# Demand constraints
for j in markets:
  m.addConstr(sum(x[i,j] for i in plants) >= demand[j])

# Production constraints
# Note that the right-hand limit sets the production to zero if the plant
# is closed
for i in plants:
  m.addConstr(sum(x[i,j] for j in markets) <= capacity[i])

# Alternative 1, using LinExpr object  
#for i in plants:
#    lhs = LinExpr(0)
#    rhs = capacity[i]
#    for j in markets:
#        lhs = lhs + x[i,j]
#    m.addConstr(lhs <= rhs)
    
# Alternative 2,
#for i in plants:
#    expr = LinExpr(sum(x[i,j] for j in markets))
#    m.addConstr(expr <= capacity[i])
 

# Solve
m.optimize()

# Print optimal cost
print m.objVal

# Print optimal solution
    
for i in plants:
    for j in markets:
        print i, j, x[i,j].x