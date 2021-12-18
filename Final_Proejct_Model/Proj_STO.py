# Second Scenario

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
Prob = np.genfromtxt("PRO_STO.csv", dtype=float, delimiter=',', encoding='utf-8-sig')
PatientSto = np.genfromtxt("Patient_STO.csv", dtype=int, delimiter=',', encoding='utf-8-sig')
transcost = 500

## Define index
hos = 14
pod = 47
scen = 10

## Model
m2 = Model()

## DV
x = m2.addVars(pod, scen, lb = 0, vtype = GRB.BINARY)
y = m2.addVars(hos, pod, scen, lb = 0, vtype = GRB.INTEGER)


##OBJ (Weighted)
z1 = LinExpr()
for i in range(hos):
    for j in range(pod):
        for k in range(scen):
            z1 += sum(sum(sum(distance[i,j] *Prob[k] * y[i,j,k])))
        
z2 = LinExpr()
for i in range(hos):
    for j in range(pod):
        for k in range(scen):
            z2 += sum(sum(sum(x[j,k]*PodCost[j]*Prob[k]+y[i,j,k]*transcost*Prob[k])))

alpha_val = [0, 0.5, 0.95,0.96, 0.97, 0.98, 0.99, 0.999, 1]

result = np.zeros([len(alpha_val),2])

for iteration in range(len(alpha_val)):
    a = alpha_val[iteration]
    # print(a)
    m2.setObjective(a*z1+(1-a)*z2, GRB.MINIMIZE)
    
    
    ## S.T.
    for i in range(hos):
        for k in range(scen):
            m2.addConstr(sum(y[i,j,k] for j in range(pod)) == PatientSto[k,i]) 
        # number of patient leaving the hospital equals to the patient supply for each hospital
    for j in range(pod):
        for k in range(scen):
            m2.addConstr(sum(y[i,j,k] for i in range(hos)) <= PodCap[j]*x[j,k]) 
        # number of patient arriving each POD should be less or equal than the pod capacity
    
    
    ## Solve
    m2.optimize()
    
    # for i in range(hos):
    #     for j in range(pod):
    #         if y[i,j,1].x != 0:
    #             print(i ,' ', j, ' ' , ' ', y[i,j,1].x, ' ', x[j,1].x)
    
    ## print result
    result[iteration, 0] = z1.getValue()
    result[iteration, 1] = z2.getValue()
    
    for j in range(pod):
        if x[j,k].x == 1:
            print('When a is', a, ' POD', j+1, ' is', x[j,k].x)
    
print(result)

plt.scatter(result[:,1], result[:,0])
            
            
    # for i in range(hos):
    #     for j in range(pod):
    #         if y[i,j,1].x != 0:
    #             z1 = sum(sum(sum(distance[i,j] *Prob[1] * y[i,j,1].x)))
    #             z2 = sum(sum(sum(x[j,1].x*PodCost[j]*Prob[1]+y[i,j,1].x*transcost*Prob[1])))
    #             print(distance[i,j], ' ', Prob[1] ,' ', y[i,j,1].x, ' ', z1,' ', z2)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            