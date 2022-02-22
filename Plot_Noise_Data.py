# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:02:05 2021

@author: AESO 1
"""

'''Modules'''
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

'''User input section'''
filename = 'C:/Users/AESO 1/Documents/Noise/Static Testing 9-21-21/9_21_20_AESO2_A.csv' #File name 
timeframe = ('11:43:01', '11:53:01') #string input time window start and end (HH:MM:SS)
y_bounds = (60, 130) #Lower and upper bounds for y axis
selections = (('11:44:18', '11:45:18'), ('11:48:48', '11:49:48'), ('11:50:18', '11:50:48'), ('11:51:27', '11:51:56')) # 2d array of selection windows in format [[start1, end1], [start2, end2],... [startn, endn]]
plot_title = 'F/A-18D Static Noise Measurement' #Title for plot
save = True #Save figure? True of False
label = False # add labels? True or False
label_angle = 30 #Degrees of rotation to plot the labels

'''End user input section'''

'''Data processing'''
data = pd.read_csv(filename, skiprows = 1, usecols = [1, 2, 3], names = ['time', 'dt', 'exp']) # Open csv file

data['time'] = data['time'].round(decimals = 0).astype(str) # Round time column down to zero and make it a string

data['time'] = pd.to_datetime(data['time'], format = '%H%M%S', exact = False).dt.time.astype(str) # Convert to timestamp format and then to string
print(data.time)
frame = {} # Window to be plotted, bound by t_0 and t_f

for i, t in enumerate(data['time']): # Find initial and final times and their corresponding indexes, put them in the frame dictionary
    if t == timeframe[0]:
        frame['t_0'] = t 
        frame['i_0'] = i
    elif t == timeframe[1]:
        frame['t_f'] = t 
        frame['i_f'] = i
    else:
        pass
    
'''General plotting controls'''
fig, ax = plt.subplots()
plt.plot(data.index, data['exp'], lw=0.8, color='black')
plt.xlim(frame['i_0'], frame['i_f'])
plt.xlabel('Time')
plt.ylabel ('Sound pressure level (dB)')
plt.yticks(fontsize=8)
plt.ylim(y_bounds[0], y_bounds[1])
ticklocs_np = np.linspace(frame['i_0'], frame['i_f'], 5) #Approximate locations for 5 evenly spaced ticks
ticklocs = [int(i) for i in ticklocs_np.tolist()]
ticklabels = [data['time'][l] for l in ticklocs] #Gets the timestamp labels for each tick location
plt.xticks(ticks=ticklocs, labels=ticklabels, rotation=0, fontsize=8, ha='left')
plt.title(plot_title)

'''Draw vertical lines'''
for s in range(len(selections)):
    s0 = [] # Selection start index
    sf = [] # Selection end index   
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'cyan', 'magenta', 'yellow', 'black']
    for i, t in enumerate(data['time']): 
        if t == selections[s][0]:
            plt.axvline(x = i, ls='--', c=colors[s], lw=1, ymin=0.1, ymax=0.9)
            s0.append(i)
            break
    for i, t in enumerate(data['time']): #get index of line 1
        if t == selections[s][1]:
            plt.axvline(x = i, ls='--', c=colors[s], lw=1, ymin=0.1, ymax=0.9)
            sf.append(i)
            break
         
    '''Calculate metrics'''        
    exp_s = data['exp'][s0[0]:sf[0]] # exponential average sound levels within selection
    Lavg_s = [10**(0.1*e) for e in exp_s] # converts exp_s from sound terms (decibel) to energy terms
    Leq = 10 * math.log((sum(Lavg_s) / len(Lavg_s)), 10)
    SEL = Leq + (10 * math.log((data['dt'][sf[0]] - data['dt'][s0[0]]), 10))
    LMAX  = max(exp_s)
    
    '''Add labels'''
    if label:
        plt.annotate('LMAX = '+str(round(LMAX, 1))+' dB\nSEL = '+str(round(SEL, 1))+' dB', xy = (s0[0]+0.005*frame['i_0'], LMAX+(0.01*y_bounds[1])), fontsize=8, rotation=label_angle) #Finds a nice place to place the labels

'''Save plot'''
if save:
    savename = filename[:-4] + '.png'
    plt.savefig(savename, dpi=1000)
        
