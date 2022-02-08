# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 12:40:45 2021

@author: AESO 1
"""

import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

file = 'C:/Users/AESO 1/Documents/TPE331-10YGD/tpe331-10ygd_ei.csv'

thrust_points = []
ff_points = []
nox_points = []
co_points = []
hc_points = []
pm_points = []

thrust = []
ff = []
nox = []
co = []
hc = []
pm = []

with open(file) as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        if row[0] == '':
            break
        thrust_points.append(float(row[0]))
        ff_points.append(float(row[1]))
        nox_points.append(float(row[2]))
        co_points.append(float(row[3]))
        hc_points.append(float(row[4]))
        pm_points.append(float(row[5]))
        
with open(file) as csvfile:
    csvreader = csv.reader(csvfile)
    for i in range(6):
        next(csvreader)
    for row in csvreader:
        if row[0] == '':
            break
        thrust.append(float(row[0]))
        ff.append(float(row[1]))
        nox.append(float(row[2]))
        co.append(float(row[3]))
        hc.append(float(row[4]))
        pm.append(float(row[5]))
        
        
# fig, ax = plt.subplots()
# plt.plot(thrust_points, ff_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(thrust, ff, color='black', lw=1.25)
# plt.xlabel('% Thrust')
# plt.ylabel('Fuel flow (lb/hr)')
# plt.xticks(ticks=np.arange(0,110,10))
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/ThrustFF.png', dpi=1000)

# "fig, ax = plt.subplots()
# plt.plot(ff_points, nox_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(ff, nox, color='black', lw=1.25)
# plt.xlabel('Fuel flow (lb/hr)')
# plt.ylabel('EI NOx (lb/1000lb fuel)')
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFNox.png', dpi=1000)

# fig, ax = plt.subplots()
# plt.plot(ff_points, co_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(ff, co, color='black', lw=1.25)
# plt.xlabel('Fuel flow (lb/hr)')
# plt.ylabel('EI CO (lb/1000lb fuel)')
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFCO.png', dpi=1000)

fig, ax = plt.subplots()
plt.plot(ff_points, hc_points, marker='o', color='black', linestyle='none', markersize='4')
plt.plot(ff, hc, color='black', lw=1.25)
plt.xlabel('Fuel flow (lb/hr)')
plt.ylabel('EI THC (lb/1000lb fuel)')
plt.yticks([0.05, 0.10, 0.15, 0.20])
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFHC.png', dpi=1000)

# fig, ax = plt.subplots()
# plt.plot(ff_points, pm_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(ff, pm, color='black', lw=1.25)
# plt.xlabel('Fuel flow (lb/hr)')
# plt.ylabel('EI PM10 (lb/1000lb fuel)')
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFPM10.png', dpi=1000)

# fig, ax = plt.subplots()
# plt.plot(ff_points, pm_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(ff, pm, color='black', lw=1.25)
# plt.xlabel('Fuel flow (lb/hr)')
# plt.ylabel('EI PM2.5 (lb/1000lb fuel)')
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFPM25.png', dpi=1000)

# fig, ax = plt.subplots()
# plt.plot(ff_points, pm_points, marker='o', color='black', linestyle='none', markersize='4')
# plt.plot(ff, pm, color='black', lw=1.25)
# plt.xlabel('Fuel flow (lb/hr)')
# plt.ylabel('EI PM (lb/1000lb fuel)')
# plt.savefig('C:/Users/AESO 1/Documents/Python Scripts/FFPM.png', dpi=1000)