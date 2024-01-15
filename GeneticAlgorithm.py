#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 23:38:25 2022

@author: nithinmadadi
"""


import numpy as np
import random
import matplotlib.pyplot as plt

 
def CreateInitialPopulation(size, cities):
    
    pop = []
    for i in range(size):
        pop.append(np.random.permutation(cities))
    return np.array(pop)



def CostOfPath(path):
    
    j = 1
    tot=0
    while ( j != len(path)):
        tot+=np.sqrt(np.sum(np.square(path[j-1] - path[j])))
        j+=1
    tot+=np.sqrt(np.sum(np.square(path[-1] - path[0])))    
    return tot




def FitnessList(population):
    
    fitness = [(i,1/(CostOfPath(population[i]))) for i in range(population.shape[0])]  
    fitness.sort(key = lambda x:x[1])    
    np_fitness = np.array(fitness) 
    
    return np_fitness



def ParentSelection(population,RankList):
    tot = sum(RankList[:,1])      
    wheel=0
    rand = random.uniform(0,tot)
    for parent_index in RankList:
        wheel += parent_index[1]       
        if wheel > rand:
            break
    return parent_index


def CrossOverAndMutation(population,RankList):
    
    NextGenSize = population.shape[0] #CHANGE HERE TO INCREASE NUMBER OF CROSSOVERS
    MutationRate = 0.1
    ElitismRate = 0.3
    DeathRate = 0.2
    Cataclysm = 0.05
    
    new_pop = []
    
    num_elite_paths = int(NextGenSize*ElitismRate)
    num_deaths = int((NextGenSize*DeathRate))
    num_crossover = int(NextGenSize) - num_elite_paths

    
    for i in range(num_crossover):
        
        p1_index = int(ParentSelection(population,RankList)[0])
        p2_index = int(ParentSelection(population,RankList)[0])
        start_index = random.randint(0, population.shape[1]-1)
        end_index = random.randint(1, population.shape[1])
        
        while end_index < start_index:
            end_index = random.randint(1, population.shape[1])
            
            
        child = [None]*(population.shape[1])
        child[start_index:end_index]=(population[p1_index].tolist())[start_index:end_index]
        
        cross_index_p2 = 0
        p2 = population[p2_index].tolist()
        for  x in range(population.shape[1]):
            if child[x] == None:
                while p2[cross_index_p2] in child:
                    cross_index_p2 += 1
                child[x] = p2[cross_index_p2]
        
        
        #MUTATION
        mut = random.uniform(0,1)
        if MutationRate > mut:
            swap1 = random.randint(0, population.shape[1]-1)
            swap2 = random.randint(0, population.shape[1]-1)
            temp = child[swap1]
            child[swap1] = child[swap2]
            child[swap2] = temp
        new_pop.append(child)


        
    #ELITISM
    for j in range(1,num_elite_paths+1):
        new_pop.append(population[int(RankList[-j,0])])

    #CATACLYSM
    # cat = random.uniform(0,1)
    # if Cataclysm > cat:
    #     new_pop = (np.random.permutation(new_pop)).tolist()
    #     new_pop = new_pop[num_deaths:]
        
        
    #     # #ADD RANDOM NEW POPULATION, FOR COMPENSATING DEATHS
    #     for r in range(num_deaths):
    #         new_pop.append(np.random.permutation(population[0]))
        
        
    return new_pop


path = "input3.txt"
with open(path,'r') as f:
    f_contents = f.read()
values_string = (f_contents.split('\n')[1:-1])
values = [[int(x) for x in i.split()] for i in values_string]
arr = np.array(values)



POP_SIZE = 20
init_pop = CreateInitialPopulation(POP_SIZE,arr)
cost_graph=[]

num_itr = 100
if init_pop.shape[1] <= 50:
    num_itr = 2150
elif init_pop.shape[1] <= 100:
    num_itr = 2260
else:
    num_itr = 680


for i in range(num_itr):
    print(i)    
    fitness_list = FitnessList(init_pop)
    cost_graph.append(CostOfPath(init_pop[int(fitness_list[-1,0])]))
    init_pop = np.array(CrossOverAndMutation(init_pop,fitness_list))



path = init_pop[int(fitness_list[-1,0])].tolist()
path.append(path[0])
file = open("output.txt", 'w')
for i,point in enumerate(path):
    string = " ".join([str(i) for i in point])
    file.write(string)
    if i != len(path)-1:
        file.write("\n")
file.close()


plt.plot(cost_graph)


