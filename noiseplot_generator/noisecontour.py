# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

# Input file options
Directory = './data/old_data/aircraft_noisefiles/csv/'                     # Directory in which data file is stored
File = 'U-6_PT6A-25_98RPM.csv'             # Name of data file 

def transpose(l1, l2):
    for i in range(len(l1[0])):
        row = []
        for item in l1:
            # appending to new list with values and index positions
            # i contains index position and item contains values
            row.append(item[i])
        l2.append(row)
    return l2

def plot_contour(path, file, extent_ft = 5000, levels = [65, 75, 85, 95], n_grids = 6, save = False):  
    radial_grids = [extent_ft*(i / (n_grids - 1)) for i in range (1, n_grids)]
    radial_grids.insert(0, 200)
    AC_ENG_PWR = []  #Aircraft name, engine, and power setting from .csv file
    data_path = path # Directory where data is stored
    data_file = file # File name
    rad= [] # The list to which the radius values are added
    azm = np.linspace(0, 360, 37) # Creates a list of 360 degrees in 10 degree increments
    sound_level = [] # The list to which sound levels are added
    not_transposed = [] # The list to which sound levels are added, before being transposed
        
    # The following block of code populates the AC_ENG_PWR list
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        for lines in csv_reader:
            AC_ENG_PWR.append(lines[0])
            AC_ENG_PWR.append(lines[1])
            AC_ENG_PWR.append(lines[2])
            break
        
    print(AC_ENG_PWR)
    
    # The following block of code populates the radius list
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader) # Skip the first line
        next(csv_reader) # skip second line
        for lines in csv_reader: # For each line of the csv file
            rad.append(float(lines[0])) # Add the first value (the radius)
            
    # The following block of code populates the sound level list
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",") 
        next(csv_reader) 
        next(csv_reader) # skip second line
        for lines in csv_reader: # For each line
            level_forward = [] # Create a blank list for sound level values
            for value in range(len(lines)): # For each value in each line
                if value == 0: # Skip the first number
                    continue
                else:
                    level_forward.append(float(lines[value])) # Add the value to level_forward
            level_reversed = level_forward[::-1] # Mirror the list of sound levels
            level_reversed.pop(0) # Remove the first value from the reversed list of sound levels, so there is no duplicate value for 180 degrees
            level_array = level_forward + level_reversed # Concatenate the forward and reversed lists
            not_transposed.append(level_array) # add level_array to the pre-transposed sound level list. The process repeats for each line
    sound_level = transpose(not_transposed, sound_level) # Transpose the data to flip the rows and columns
    r, th = np.meshgrid(rad, np.radians(azm)) # Create a grid to plot the sound levels on
    
    # Plotting controls
    labels = [str(levels[l]) for l in range(len(levels))] #turns the levels list into a list of strings, so it can be read by the legend
    grid_labels_raw = [str("{:,g}".format(radial_grids[g])) + ' ft.' for g in range(len(radial_grids))] #turns the radial grids list into a list of strings, so it can be read by the legend
    grid_labels = []
    
    if len(radial_grids) % 2 == 1: # if there is an odd number of grids, arrange labels like so
        for l in range(len(grid_labels_raw)): #alternate label and empty space for radial grids
            if l % 2 == 0:
                grid_labels.append(grid_labels_raw[l])
            else:
                grid_labels.append('')
    else: #if there is an even number of grids, arrange labels like so
        for l in range(len(grid_labels_raw)): #alternate label and empty space for radial grids
            if l % 2 == 1:
                grid_labels.append(grid_labels_raw[l])
            else:
                grid_labels.append('')
                
    
    grid_labels[0] = '' # makes the first grid label a blank space, to de-clutter the plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar')) # Create a polar plot
    
    CS = ax.contour(th, r, sound_level, levels=levels, colors=('blue', 'green', 'orange', 'red', 'purple', 'black'), linewidths=.8, zorder=3)

    arrow_position = []
    if len(radial_grids) == 4:
        arrow_position.append(2.5)
    elif len(radial_grids) == 5:
        arrow_position.append(1.5)
    elif len(radial_grids) == 6:
        arrow_position.append(1.5)
    elif len(radial_grids) == 3:
        arrow_position.append(4)
    elif len(radial_grids) == 7:
        arrow_position.append(1.5)
        
    arr2 = plt.arrow(0, (radial_grids[1]+radial_grids[2])/arrow_position[0], 0, radial_grids[-1]*0.06, alpha = 1, width = 0.0, edgecolor = 'black', facecolor='black', overhang=.50, lw = 0, shape='full', zorder = 2, length_includes_head=False, head_width=0.13, head_length=radial_grids[-1]*0.06)

    
    plot_title = [r"$\bf{" + AC_ENG_PWR[0] + "}$" + '\n' + AC_ENG_PWR[1] + '\n' + AC_ENG_PWR[2]]  # Plot title
    ax.set_title(plot_title[0], x=-.11, pad=8, loc='left',fontsize=10)
    plt.rgrids((radial_grids), (grid_labels), angle=75, fontsize=5, color='#5E5B5B',zorder=1000) #Radial grids + grid labels are added here
    
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
#Call the function with the directory and filename as inputs
plot_contour(Directory, File) 
plt.savefig("/mnt/c/Users/gregory.bizup/Pictures/static.png", bbox_inches='tight', dpi=1000)
plt.show()

