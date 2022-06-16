# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import numpy as np
import csv
import pandas as pd
import re

def plot_contour(df, aircraft, engine, description, power, extent_ft = 5000, 
                 levels = [65, 75, 85, 95], n_grids = 6, save_name = None):  
    
    levels = sorted(list(set(levels))) # Remove duplicates, sort ascending
    
    n_grids = n_grids if n_grids < 50 else 50 # Max 100 grids to prevent crash
    radial_grids = [extent_ft*(i / (n_grids - 1)) for i in range (1, n_grids)] if n_grids > 2 else [extent_ft]
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
        
    arr2 = plt.arrow(0, radial_grids[-1]/1.5, 0, radial_grids[-1]*0.06, 
                     alpha = 1, width = 0.0, edgecolor = 'black', facecolor='black', 
                     overhang=.50, lw = 0, shape='full', zorder = 2, length_includes_head=False, 
                     head_width=0.13, head_length=radial_grids[-1]*0.06)

    
    plot_title = r"$\bf{" + aircraft + "}$" + '\n' + engine + '\n' + description + '\n' + power 
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
    if save_name:
        plt.savefig(save_name, bbox_inches = 'tight', dpi = 500)   
    plt.tight_layout()
    
    return(fig)
    
def fmt_line_plot(ax):
    plt.grid(axis='x', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='x', color='0.8', linewidth=0.5)
    plt.grid(axis='y', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='y', color='0.8', linewidth=0.5)
    plt.xticks(fontsize=8,                                            
        ticks=[0, 5000, 10000, 15000, 20000, 25000],                  
        labels=['0', '5,000', '10,000', '15,000', '20,000', '25,000'])
    plt.xlabel('Slant distance (ft.)', fontsize=8)
    plt.ylabel('SEL & LAMAX (dB)')
    plt.yticks(fontsize=8)
    plt.xlim(0, 26000)
    plt.ylim(20, 140)
    ax.xaxis.set_minor_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.set_facecolor('#f8f8ff')

def fmt_line_title(ax, df, df_2 = None, ps_name = None, spd = 160):
    # Construct power setting string based on arguments
    power = "{} ({} - {}{})".format(ps_name, df.pwr[0], 
                                        df_2.pwr[0], df.unit[0])           \
            if ps_name is not None and df_2 is not None else               \
            "{} ({} - {}{})".format(df.desc[0], df.pwr[0], 
                                        df_2.pwr[0], df.unit[0])           \
            if ps_name is None and df_2 is not None else                   \
            "{} ({}{})".format(ps_name, df.pwr[0], df.unit[0])           \
            if ps_name is not None and df_2 is None else                   \
            "{} ({}{})".format(df.desc[0], df.pwr[0], df.unit[0])        
    power = re.sub("%", "\\%", power) # Escape special characters
    power = re.sub(" ", "\\ ", power)
    title_1 = r"$\bf{" + df.ac[0]     + "}$" + '\n' + df.eng[0]
    title_2 = r"$\bf{" + power + "}$" + '\n' + str(spd) + " kts."
    ax.set_title(title_1, pad=8, loc='left',fontsize=10)
    ax.set_title(title_2, pad=8, loc='right',fontsize=10)  

def fmt_line_leg(ax, df_1 = None, df_2 = None):
    leg = ax.legend(["SEL ({}{})".format(df_1.pwr[0], df_1.unit[0]),       \
                     "LAMAX ({}{})".format(df_1.pwr[0], df_1.unit[0]),     \
                     "SEL ({}{})".format(df_2.pwr[0], df_2.unit[0]),       \
                     "LAMAX ({}{})".format(df_2.pwr[0], df_2.unit[0])],    \
                     fontsize = 7, ncol = 2)                               \
                     if df_1 is not None and df_2 is not None else         \
                     ax.legend(["LMAX", "SEL"], fontsize = 8)
    leg.set_title("Noise metric", prop = {"size" : 8})
    leg.get_frame().set_edgecolor("black")

def plot_line(df, df_2 = None, ps_name = None, save_name = None, spd = 160): #df from interpolate()
    fig, ax = plt.subplots()
    if df_2 is not None: # If two dataframes are detected, make a filled plot
        plt.plot(df.dist, df.sel, "C0-", df.dist, df.lmax, "C1-",
            lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
        plt.plot(df_2.dist, df_2.sel, "C0--", df_2.dist, df_2.lmax, "C1--",
            lw = 0.7, markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
        ax.fill_between(df.dist, df.sel,  df_2.sel, color = "C0",  alpha=0.5, zorder=3)
        ax.fill_between(df.dist, df.lmax, df_2.lmax, color= "C1", alpha=0.5, zorder=3)    
    else: # Else just make a line plot
        plt.plot(df.dist, df.lmax, "o-", df.dist, df.sel, "x-", linewidth = 0.7,
             markerfacecolor = 'none', markeredgewidth = 0.7, ms = 4)
    fmt_line_plot(ax)
    fmt_line_title(ax, df, df_2, ps_name = ps_name, spd = spd)
    fmt_line_leg(ax, df, df_2)
    if save_name:
        plt.savefig(save_name, bbox_inches = 'tight', dpi = 500)
    return(fig)

