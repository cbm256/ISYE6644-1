# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 21:27:47 2020

@author: rachh
"""
import random
import math
import pandas as pd
from collections import defaultdict 
import numpy as np
import matplotlib.pyplot as plt

def die_toss(rand):
    roll=math.ceil(6*rand)
    return roll 

def outcome(roll,pot):
    if roll==2:
        coins=pot
        pot-=coins
    elif roll==3:
        coins=math.floor(pot/2)
        pot-=coins
    elif roll in range(4,7):
        coins=-1
        pot+=1
    else:
        coins=0
    if pot<0:
        pot=0
    return coins,pot  

def game():
    A_coins=[4]
    B_coins=[4]
    A_roll=[]
    B_roll=[]
    pot_total=[2]
    player_A=4
    player_B=4
    count=0
    exception=0
    while exception ==0: 
        pot=pot_total[count]
        toss_A=die_toss(random.random())
        A_roll.append(toss_A)
        if toss_A in range(4,7) and player_A==0:
            player_A=-1
            count+=1
            A_coins.append(player_A)
            exception=1
            break
        else:
            outcome_A=outcome(toss_A,pot)
            
            player_A+=outcome_A[0]
            A_coins.append(player_A)
            
        toss_B=die_toss(random.random())
        B_roll.append(toss_B)
        if toss_B in range(4,7) and player_B==0:
            player_B=-1
            pot_total.append(outcome_A[1])
            count+=1
            B_coins.append(player_B)
            exception=1
            break
        else:
            outcome_B=outcome(toss_B,outcome_A[1])
            player_B+=outcome_B[0]
            B_coins.append(player_B)
            pot_total.append(outcome_B[1])
            count+=1
        cycle_length=count+1
    return cycle_length, A_coins, B_coins, A_roll, B_roll, pot_total


def same_length(x,y):
    if len(x)>len(y):
        l=len(x)
        a=x
        b=y
        b.append(b[l-2])
    else:
        a=x
        b=y
    return x,y 

chain={}   
def tuple_dict(z):
    n_tuples=len(z)
    for i, key in enumerate(z):
        if n_tuples > (i+1):
            tup=z[i+1]
            if key not in chain:
                chain[key]=[tup]
            else:
                chain[key].append(tup)
    return chain 

cycle_lengths=[]                
for i in range(1000):
    g=game()
    cycle_lengths.append(g[0])
    x,y=same_length(g[1],g[2])
    v=list(zip(x,y))
    tuple_dict(v)
  

    
names=dict.keys(chain)
df=pd.DataFrame(index=names,columns=names)

for k in dict.keys(chain):
    for l in chain[k]:
        df.at[k,l]=chain[k].count(l)
    
    
df2=(df.T / df.T.sum()).T
df2=df2.fillna(0)
df2=df2.iloc[:,:66]
I=np.identity(66)
df3=df2.to_numpy(dtype=np.float)
M=I-df3
N=np.linalg.inv(M)
E=N[0].sum()


_ = plt.hist(cycle_lengths, density=1, bins=20)
mean_cycles=np.mean(cycle_lengths)
p_hat=1/(np.mean(cycle_lengths))


plt.show()
print(f'The expected value from first step analysis is {E}.')
print(f'The value of the point estimator, p-hat, is approximately {p_hat}, and the mean number of cycles from the data is {mean_cycles}.')