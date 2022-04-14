# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 12:40:45 2021

@author: AESO 1
"""

import matplotlib.pyplot as plt
import pandas as pd

file = 'C:/Users/AESO 1/Documents/TPE331-10YGD/tpe331-10ygd_ei.csv'

pts = pd.read_csv(file, nrows=4)
line = pd.read_csv(file, skiprows=6, names=pts.columns)
        
print(pts.columns[2:])

fig, ax = plt.subplots()
plt.plot(pts['%Thrust'], pts['FF'], marker='o', color='black', linestyle='none', markersize='4')
plt.plot(line['%Thrust'], line['FF'], color='black', lw=1.25)
plt.xlabel('% Thrust')
plt.ylabel('Fuel flow (lb/hr)')
#plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/ThrustFF.png', dpi=1000)
       
for c in pts.columns[2:]:
    fig, ax = plt.subplots()
    plt.plot(pts['FF'], pts[c], marker='o', color='black', linestyle='none', markersize='4')
    plt.plot(line['FF'], line[c], color='black', lw=1.25)
    plt.xlabel('% Thrust')
    plt.ylabel('Fuel flow (lb/hr)')
    #plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/ThrustFF.png', dpi=1000)
        