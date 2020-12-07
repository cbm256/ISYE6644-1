# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:11:47 2020

@author: rmhastreiter
"""

import random
import math
import numpy as np
import scipy.stats as st

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

Z_r=[]
for i in range(30):
    cycles=[]
    for j in range(100):
        cycles.append(game()[0])
    Z_r.append(np.mean(cycles))

CI_mean=st.t.interval(alpha=0.95, df=len(Z_r)-1, loc=np.mean(Z_r), scale=st.sem(Z_r)) 
print(f'The 95% confidence interval for the mean number of cycles the game will last is {CI_mean}.')





