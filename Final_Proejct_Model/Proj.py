# First Scenario

from gurobipy import *
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd


## Read Data
PodCost = np.genfromtxt("PodCost.csv", dtype=int, delimiter=',', encoding='utf-8-sig')
PodCap = np.genfromtxt("PodCap.csv", dtype=int, delimiter=',', encoding='utf-8-sig')
HosCap = np.genfromtxt("HosCap.csv", dtype=int, delimiter=',', encoding='utf-8-sig')
distance = np.genfromtxt("POD_DISTANCE.csv", dtype=float, delimiter=',', encoding='utf-8-sig') # In km
patient = np.genfromtxt("patients_number.csv", dtype=int, delimiter=',', encoding='utf-8-sig')
transcost = 500

## Define index
hos = 14
pod = 47


## Model
m1 = Model()


## DV
x = m1.addVars(pod, lb = 0, vtype = GRB.BINARY)
y = m1.addVars(hos, pod, lb = 0, vtype = GRB.INTEGER)


##OBJ (Weighted)
z1 = LinExpr()
for i in range(hos):
    for j in range(pod):
        z1 += sum(sum(distance[i,j] * y[i,j]))
        
z2 = LinExpr()
for i in range(hos):
    for j in range(pod):
        z2 += sum(sum(x[j]*PodCost[j]+y[i,j]*transcost))

alpha_val = [0, 
              # 0.5,
              # 0.95,
              # 0.96,
              # 0.97,
              # 0.98,
              0.99,
              0.999,
              1]

result = np.zeros([len(alpha_val),2])

for iteration in range(len(alpha_val)):
    a = alpha_val[iteration]
    # print(a)
    m1.setObjective(a*z1+(1-a)*z2, GRB.MINIMIZE)
    
    
    ## S.T.
    for i in range(hos):
        m1.addConstr(sum(y[i,j] for j in range(pod)) == patient[i]) 
        # number of patient leaving the hospital equals to the patient supply for each hospital
    for j in range(pod):
        m1.addConstr(sum(y[i,j] for i in range(hos)) <= PodCap[j]*x[j]) 
        # number of patient arriving each POD should be less or equal than the pod capacity
    
    
    ## Solve
    m1.optimize()
    
    ## print result
    result[iteration, 0] = z1.getValue()
    result[iteration, 1] = z2.getValue()
    
    # for j in range(pod):
    #     if x[j].x == 1:
    #         print('When a is', a, ' POD', j+1, ' is', x[j].x)
    for i in range(hos):
        for j in range(pod):
            if y[i,j].x != 0:
                print(i,' ',j,' ',y[i,j].x)
    
print(result)

plt.scatter(result[:,1], result[:,0])

################################################################################




