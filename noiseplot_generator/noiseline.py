# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import csv
import os
import pandas as pd

''' BEGIN USER INPUT '''

# Plot controls
#plot_type = "filled" # Choose plot type. "filled", "line", or "all"
#Description = 'Cruise' # power description (filled)
#Range = [84, 96] # power setting (filled)
#Power_units = '% NC' # power setting units (filled)
#
## File controls
#Dir1 = '../python-tools/data/csv/Flight/' # Directory for data file (used in filled and line)
#File1 = 'F-18EF_F414-GE-400_84NC.csv' # data file (used in filled and line)
#Dir2 = '../python-tools/data/csv/Flight/' # directory (used as second directory for filled)
#File2 = 'F-18EF_F414-GE-400_96NC.csv' #file (used as second data file for line)
#Dir_all = '../python-tools/data/csv/Flight/'   # Plot all the data files in this directory (Plot all only)
#
## Save controls
#Save = True                      # Save figure? (True or False)
#save_dir = './savetest-all/' # directory to save plot
#save_name = 'F-18_line_3-31-22_savetest' # name for image

''' END USER INPUT '''

def list_aircraft(dir = "./data/csv/Flight/"):
    files = os.listdir(dir)
    ac = set([f.split("_", 1)[0] for f in files])
    return list(ac)

def format_plot():
    plt.grid(axis='x', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='x', color='0.8', linewidth=0.5)
    plt.grid(axis='y', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='y', color='0.8', linewidth=0.5)
    plt.xticks(fontsize=8, ticks=[0, 5000, 10000, 15000, 20000, 25000], labels=['0', '5,000', '10,000', '15,000', '20,000', '25,000'])
    plt.xlabel('Slant distance (ft.)', fontsize=8)
    plt.ylabel('SEL & LAMAX (dB)')
    plt.yticks(fontsize=8)
    plt.xlim(0, 26000)
    plt.ylim(20, 140)

def plot_line(path, file, save = False, save_dir = "./", save_name = "line_plot"):  
    
    ac_data = pd.read_csv(path + file, nrows=1, usecols=[0, 1, 2, 3], names= ['Aircraft', 'Engine', 'Power', 'Speed'])
    noise_data = pd.read_csv(path + file, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(noise_data['Distance'], noise_data['SEL'], 'o-', noise_data['Distance'], noise_data['ALM'], 'x-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + ac_data['Aircraft'][0] + "}$" + '\n' + ac_data['Engine'][0]]  # Plot title
    plot_title_2 = [ac_data['Power'][0] + '\n' + ac_data['Speed'][0]]
    ax.set_title(plot_title[0], pad=8, loc='left',fontsize=10)
    ax.set_title(plot_title_2[0], pad=8, loc='right',fontsize=10)
    ax.xaxis.set_minor_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.set_facecolor('#f8f8ff')
    leg = ax.legend(['SEL', 'LAMAX'], fontsize=8)
    leg.set_title("Noise metric",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    format_plot()

    if save:
        plt.savefig(save_dir+save_name+'.png', bbox_inches='tight', dpi=1000)

    # isDir = os.path.isdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0]) #check if aircraft directory exists
    # if isDir == False: # if aircraft directory does not exist, make it
    #     os.mkdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0])

def plot_filled(path, file, path_2, file_2, Range, Power_units = "%", save = False, save_dir = "./", save_name = "filled_plot"):  
    
    ac_data_1 = pd.read_csv(path + file, nrows=1, usecols=[0, 1, 2, 3], names= ['Aircraft', 'Engine', 'Power', 'Speed'])
    noise_data_1 = pd.read_csv(path + file, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
    noise_data_2 = pd.read_csv(path_2 + file_2, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(noise_data_1['Distance'], noise_data_1['SEL'], 'C0-', noise_data_1['Distance'], noise_data_1['ALM'], 'C1-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plt.plot(noise_data_2['Distance'], noise_data_2['SEL'], 'C0--', noise_data_2['Distance'], noise_data_2['ALM'], 'C1--', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + ac_data_1['Aircraft'][0] + "}$" + '\n' + ac_data_1['Engine'][0]]  # Plot title
    plot_title_2 = [Description + ' (' + str(Range[0]) + ' - ' + str(Range[1]) + Power_units + ')' + '\n' + ac_data_1['Speed'][0]]
    ax.set_title(plot_title[0], pad=8, loc='left',fontsize=10)
    ax.set_title(plot_title_2[0], pad=8, loc='right',fontsize=10)
    plt.grid(axis='x', which='minor', color='0.85', linewidth=0.3, zorder=0)
    plt.grid(axis='x', color='0.8', linewidth=0.5, zorder=0)
    plt.grid(axis='y', which='minor', color='0.85', linewidth=0.3, zorder=0)
    plt.grid(axis='y', color='0.8', linewidth=0.5, zorder=0)
    plt.xticks(fontsize=8, ticks=[0, 5000, 10000, 15000, 20000, 25000], labels=['0', '5,000', '10,000', '15,000', '20,000', '25,000'])
    ax.xaxis.set_minor_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    plt.xlabel('Slant distance (ft.)', fontsize=8)
    plt.ylabel('SEL & LAMAX (dB)')
    plt.yticks(fontsize=8)
    plt.xlim(0, 26000)
    plt.ylim(20, 140)
    ax.set_facecolor('#f8f8ff')
    #h1,l1 = plt.legend_elements() #legend
    leg = ax.legend(['SEL (' + str(Range[0]) + Power_units + ')', 'LAMAX (' + str(Range[0]) + Power_units + ')', 'SEL (' + str(Range[1]) + Power_units + ')', 'LAMAX (' + str(Range[1]) + Power_units + ')'], fontsize=7, ncol=2)
    leg.set_title("Noise metric",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    ax.fill_between(noise_data_1['Distance'], noise_data_1['SEL'], noise_data_2['SEL'], alpha=0.5, zorder=3)
    ax.fill_between(noise_data_1['Distance'], noise_data_1['ALM'], noise_data_2['ALM'], alpha=0.5, zorder=2)
    
    if save:
        plt.savefig(save_dir+save_name+'.png', bbox_inches='tight', dpi=1000)

def plot_all(Dir, save = False):
    Name_list = os.listdir(Dir)
    for filename in Name_list:
        AC_NAME = [] #Get the name of the current aircraft to add it to the Destination variable
        with open(Dir+filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for lines in csv_reader:
                AC_NAME.append(lines[0])
                break
        
        plot_line(Dir, filename) 
        print(filename)
        Destination = Dir+filename[:-4]+'.png'
        print(Destination)
        if save:
            plt.savefig(Destination, bbox_inches='tight', dpi=1000)
       

#if plot_type == "filled":
#    plot_filled(Dir1, File1, Dir2, File2, Save)
#elif plot_type == "line":
#    plot_line(Dir1, File1, Save)
#elif plot_type == "all":
#    plot_all(Dir_all, Save)
