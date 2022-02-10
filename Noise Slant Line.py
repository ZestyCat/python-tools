# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import csv
import os
import pandas as pd

''' BEGIN USER INPUT '''

# Line plot controls
Directory = 'C:/Users/AESO 1/Documents/Noise/csv/Flight/Omega10_2-2-20/'                    # Directory in which data file is stored

# Filled plot controls
Dir1 = 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/'
Dir2 = 'A-6A_J57-P-8A_94RPM.csv'
File1 = 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/'
File2 = 'A-6A_J57-P-8A_89RPM.csv'
Description = 'Cruise'
Range = '90 - 95% RPM'

# Save controls
Save = 1                      # Save figure? (1 for yes, 0 for no)
save_dir = 'C:/Users/AESO 1/Documents/Noise/' #directory to save plot
save_name = 'A-3_range-pd-test'

''' END USER INPUT '''


def plot_line(path, file):  
    
    ac_data = pd.read_csv(path + file, nrows=1, usecols=[0, 1, 2, 3], names= ['Aircraft', 'Engine', 'Power', 'Speed'])
    noise_data = pd.read_csv(path + file, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(noise_data['Distance'], noise_data['SEL'], 'o-', noise_data['Distance'], noise_data['ALM'], 'x-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + ac_data['Aircraft'][0] + "}$" + '\n' + ac_data['Engine'][0]]  # Plot title
    plot_title_2 = [ac_data['Power'][0] + '\n' + ac_data['Speed'][0]]
    ax.set_title(plot_title[0], pad=8, loc='left',fontsize=10)
    ax.set_title(plot_title_2[0], pad=8, loc='right',fontsize=10)
    plt.grid(axis='x', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='x', color='0.8', linewidth=0.5)
    plt.grid(axis='y', which='minor', color='0.85', linewidth=0.3)
    plt.grid(axis='y', color='0.8', linewidth=0.5)
    plt.xticks(fontsize=8, ticks=[0, 5000, 10000, 15000, 20000, 25000], labels=['0', '5,000', '10,000', '15,000', '20,000', '25,000'])
    ax.xaxis.set_minor_locator(MultipleLocator(1000))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    plt.xlabel('Slant distance (ft.)', fontsize=8)
    plt.ylabel('SEL & LAMAX (dB)')
    plt.yticks(fontsize=8)
    plt.xlim(0, 26000)
    plt.ylim(20, 140)
    ax.set_facecolor('#f8f8ff')
    leg = ax.legend(['SEL', 'LAMAX'], fontsize=8)
    leg.set_title("Noise metric",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    
    # isDir = os.path.isdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0]) #check if aircraft directory exists
    # if isDir == False: # if aircraft directory does not exist, make it
    #     os.mkdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0])

def plot_filled(path, file, path_2, file_2):  
    
    ac_data_1 = pd.read_csv(path + file, nrows=1, usecols=[0, 1, 2, 3], names= ['Aircraft', 'Engine', 'Power', 'Speed'])
    noise_data_1 = pd.read_csv(path + file, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
    noise_data_2 = pd.read_csv(path_2 + file_2, skiprows=[0, 1, 2], usecols=[0, 1, 5], names = ['Distance', 'SEL', 'ALM'])
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(noise_data_1['Distance'], noise_data_1['SEL'], 'C0-', noise_data_1['Distance'], noise_data_1['ALM'], 'C1-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plt.plot(noise_data_2['Distance'], noise_data_2['SEL'], 'C0-', noise_data_2['Distance'], noise_data_2['ALM'], 'C1-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + ac_data_1['Aircraft'][0] + "}$" + '\n' + ac_data_1['Engine'][0]]  # Plot title
    plot_title_2 = [Description + ' (' + Range + ')' + '\n' + ac_data_1['Speed'][0]]
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
    leg = ax.legend(['SEL', 'LAMAX'], fontsize=8)
    leg.set_title("Noise metric",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    ax.fill_between(noise_data_1['Distance'], noise_data_1['SEL'], noise_data_2['SEL'], alpha=0.5, zorder=3)
    ax.fill_between(noise_data_1['Distance'], noise_data_1['ALM'], noise_data_2['ALM'], alpha=0.5, zorder=2)
    
    if Save == 1:
            plt.savefig(save_dir+save_name+'.png', bbox_inches='tight', dpi=1000)


# def plot_all():
#     Name_list = os.listdir(Directory)
#     for filename in Name_list:
#         AC_NAME = [] #Get the name of the current aircraft to add it to the Destination variable
#         with open(Directory+filename) as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=",")
#             for lines in csv_reader:
#                 AC_NAME.append(lines[0])
#                 break
        
#         plot_line(Directory, filename) 
#         print(filename)
#         Destination = Directory+filename[:-4]+'.png'
#         print(Destination)
#         if Save == 1:
#             plt.savefig(Destination, bbox_inches='tight', dpi=1000)
                
plot_filled('C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/', 'A3_J57-P-10_90RPM.csv', 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/', 'A3_J57-P-10_95RPM.csv')
