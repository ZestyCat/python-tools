# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 11:02:05 2021

@author: AESO 1
"""

'''User input section'''

filename = 'C:/Users/AESO 1/Documents/Noise/Static Testing 9-21-21/9_21_20_AESO1_C.csv' #File name 
t_0 = '11:43:01' #string input time window start (HH:MM:SS)
t_f = '11:53:01' #string input time window end (HH:MM:SS)
y_lower = 60 #Lower bounds for y axis
y_upper = 130 #Upper bounds for y axis
save = 'false' #Save figure? True for yes
selections = [['11:44:18', '11:45:18'], ['11:48:48', '11:49:48'], ['11:50:18', '11:50:48'], ['11:51:33', '11:51:56']] # 2d array of selection windows in format [[start1, end1], [start2, end2],... [startn, endn]]
label_angle = 30 #Degrees of rotation to plot the labels
plot_title = 'F/A-18D Static Noise Measurement' #Title for plot

'''End user input section'''

'''Modules'''
import csv
import matplotlib.pyplot as plt
import math
import numpy as np

'''Variables'''
ntime = [] #Measurement number and corresponding time
n = [] #Measurement number 
exp = [] #Exponential average in dB
dt = [] #Elapsed time (s)
ntimestamp = [] # Measurement number and timestamp
nt0 = [] #Measurement number and corresponding timestamp (initial)
ntf = [] #Measuremnt number and corresponding timestamp (final)
ticks = [] #Equally spaced timestamps for the xticks labels

'''Read csv data'''
with open(filename) as file: #Open data file
    reader = csv.reader(file) #Create csv reader object
    next(reader)
    for row in reader: #Get data
        nt = [int(float(row[0]))-1, row[1]]
        ntime.append(nt)
        n.append(int(float(row[0])))
        exp.append(float(row[3]))
        dt.append(float(row[2]))
        
'''Parse timestamp'''
for t in range(len(ntime)): #parse the time data into a readable format
    for i in range(len(ntime[t][1])): #find location of the decimal
        d = ntime[t][1].find('.') 
        if d == 6: #For timestamps with 6 numbers to the left of the decimal
            nstamp = [ntime[t][0], ntime[t][1][d-6:d-4] + ':' + str(ntime[t][1][d-4:d-2]) + ':' + str(ntime[t][1][d-2:d]) + str(ntime[t][1][d:d+3])]
            ntimestamp.append(nstamp)
        elif d == 5: #For timestamps with 5 numbers to the left of the decimal, add a zero at the beginning (e.g. 08:47:36)
            nstamp = [ntime[t][0], '0' + str(ntime[t][1][d-5:d-4]) + ':' + str(ntime[t][1][d-4:d-2]) + ':' + str(ntime[t][1][d-2:d]) + str(ntime[t][1][d:d+3])]
            ntimestamp.append(nstamp)
        break
    
'''Get indexes for window t0, tf'''
for i in range(len(ntimestamp)): #get index of t_0
    if ntimestamp[i][1][:-3] == t_0:
        initial = [ntimestamp[i][0], ntimestamp[1][1]]
        nt0.append(initial) #Measurement number and timestamp at t0
        break
for i in range(len(ntimestamp)): #get index of t_f
    if ntimestamp[i][1][:-3] == t_f:
        final = [ntimestamp[i][0], ntimestamp[i][1]]
        ntf.append(final) #Measurement number and timestamp at tf
        break

'''General plotting controls'''
fig, ax = plt.subplots()
plt.plot(n, exp, lw=0.8, color='black')
plt.xlim(nt0[0][0],ntf[0][0])
plt.xlabel('Time')
plt.ylabel ('Sound pressure level (dB)')
plt.yticks(fontsize=8)
plt.ylim(y_lower, y_upper)
ticklocs_np = np.linspace(nt0[0][0], ntf[0][0], 5) #Approximate locations for 5 evenly spaced ticks
ticklocs = [int(i) for i in ticklocs_np.tolist()]
ticklabels = [ntimestamp[l][1][:-3] for l in ticklocs] #Gets the timestamp labels for each tick location
plt.xticks(ticks=ticklocs, labels=ticklabels, rotation=0, fontsize=8, ha='left')
plt.title(plot_title)

'''Draw vertical lines'''
for s in range(len(selections)):
    s0 = [] # Selection start index
    sf = [] # Selection end index   
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'cyan', 'magenta', 'yellow', 'black']
    for i in range(len(ntimestamp)): #get index of line 1
        if ntimestamp[i][1][:-3] == selections[s][0]:
            plt.axvline(x=ntimestamp[i][0], ls='--', c=colors[s], lw=1, ymin=0.1, ymax=0.9)
            s0.append(ntimestamp[i][0])
            break
    for i in range(len(ntimestamp)): #get index of line 1
        if ntimestamp[i][1][:-3] == selections[s][1]:
            plt.axvline(x=ntimestamp[i][0], ls='--', c=colors[s], lw=1, ymin=0.1, ymax=0.9)
            sf.append(ntimestamp[i][0])
            break
                
    '''Calculate metrics'''        
    exp_s = exp[s0[0]:sf[0]] # exponential average sound levels within selection
    Lavg_s = [10**(0.1*e) for e in exp_s] # converts exp_s from sound terms (decibel) to energy terms
    Leq = 10 * math.log((sum(Lavg_s) / len(Lavg_s)), 10)
    SEL = Leq + (10 * math.log((dt[sf[0]] - dt[s0[0]]), 10))
    LMAX  = max(exp_s)
    
    '''Add labels'''
    plt.annotate('LMAX = '+str(round(LMAX, 1))+' dB\nSEL = '+str(round(SEL, 1))+' dB', xy = (s0[0]+0.005*ntf[0][0], LMAX+(0.01*y_upper)), fontsize=8, rotation=label_angle) #Finds a nice place to place the labels

'''Save plot'''
if save == 'true':
    savename = filename[:-4] + '.png'
    plt.savefig(savename, dpi=1000)

        
