# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import functions as fn

def plot_contour(df, aircraft, engine, power, extent_ft = 5000, 
                 levels = [65, 75, 85, 95], n_grids = 6, save = False):  
    
    radial_grids = [extent_ft*(i / (n_grids - 1)) for i in range (1, n_grids)]
    radial_grids.insert(0, 200)
    azm = np.linspace(0, 360, 37)
    rad = df.index.values.tolist()
    r, th = np.meshgrid(rad, np.radians(azm)) # Create a grid to plot the sound levels on

    labels = [str(levels[l]) for l in range(len(levels))] 
    all_grid_labels = [str("{:,g}".format(radial_grids[g])) + ' ft.' for g in range(len(radial_grids))] 
    grid_labels = []
    
    if len(radial_grids) % 2 == 1: # if there is an odd number of grids, arrange labels like so
        for l in range(len(all_grid_labels)): #alternate label and empty space for radial grids
            if l % 2 == 0:
                grid_labels.append(all_grid_labels[l])
            else:
                grid_labels.append('')
    else: #if there is an even number of grids, arrange labels like so
        for l in range(len(all_grid_labels)): #alternate label and empty space for radial grids
            if l % 2 == 1:
                grid_labels.append(all_grid_labels[l])
            else:
                grid_labels.append('')
    
    grid_labels[0] = '' # makes the first grid label a blank space, to de-clutter the plot
    
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar')) # Create a polar plot
    
    sound_levels = pd.concat([df.T, df.T.iloc[::-1][1:]])# appends reversed df to fill 360 degrees
    CS = ax.contour(th.tolist(), r.tolist(), sound_levels, levels=levels, 
                    colors=('blue', 'green', 'orange', 'red', 'purple', 'black'), 
                    linewidths=.8, zorder=3)

    arrow_position = 2.5 if len(radial_grids) == 4 else \
                     1.5 if len(radial_grids) == 5 else \
                     1.5 if len(radial_grids) == 6 else \
                     4.0 if len(radial_grids) == 3 else \
                     1.5 if len(radial_grids) == 7 else 1.5
        
    arr2 = plt.arrow(0, (radial_grids[1]+radial_grids[2])/arrow_position, 0, radial_grids[-1]*0.06, 
                     alpha = 1, width = 0.0, edgecolor = 'black', facecolor='black', 
                     overhang=.50, lw = 0, shape='full', zorder = 2, length_includes_head=False, 
                     head_width=0.13, head_length=radial_grids[-1]*0.06)

    
    plot_title = r"$\bf{" + aircraft + "}$" + '\n' + engine + '\n' + power 
    ax.set_title(plot_title, x=-.11, pad=8, loc='left',fontsize=10)
    plt.rgrids((radial_grids), (grid_labels), angle=75, fontsize=5, color='#5E5B5B',zorder=1000)    

    ygrids = ax.get_ygridlines() #make gridlines smaller
    for g in ygrids:
        #g.set_color('red')
        g.set_linewidth(0.4)
    
    xgrids = ax.get_xgridlines()
    for g in xgrids:
        g.set_linewidth(0.4)
    
    plt.ylim(0,radial_grids[-1]) # Sets the y limits to the highest radial grid
    plt.xticks(fontsize=8)
    ax.set_facecolor('#f8f8ff')
    h1,l1 = CS.legend_elements()
    leg = ax.legend(h1, labels, title="LAMAX (dBA)", facecolor='#f8f8ff', fontsize=8, bbox_to_anchor=(1.2, 1.28))
    leg.set_title("LAMAX (dBA)",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    
    return(fig)
