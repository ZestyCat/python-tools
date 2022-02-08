# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import csv
import os

''' BEGIN USER INPUT '''

# Line plot controls
Directory = 'C:/Users/AESO 1/Documents/Noise/csv/Flight/Omega10_2-2-20/'                    # Directory in which data file is stored
Save = 1                      # Save figure? (1 for yes, 0 for no)

# Filled plot controls
Dir1 = 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/'
Dir2 = 'A-6A_J57-P-8A_94RPM.csv'
File1 = 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/'
File2 = 'A-6A_J57-P-8A_89RPM.csv'
Description = 'Cruise'
Range = '90 - 95% RPM'

''' END USER INPUT '''


def plot_line(path, file):  
    
    AC_ENG_PWR_SPEED = []  #Aircraft name, engine, and power setting from .csv file
    data_path = path # Directory where data is stored
    data_file = file # File name
    D_ft = [] #Slant distance
    SEL_dB = [] #A-G SEL/LAMAX
    LAMAX_dB = []
    
    # The following block of code populates the AC_ENG_PWR_SPEED list
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        for lines in csv_reader:
            AC_ENG_PWR_SPEED.append(lines[0])
            AC_ENG_PWR_SPEED.append(lines[1])
            AC_ENG_PWR_SPEED.append(lines[2])
            AC_ENG_PWR_SPEED.append(lines[3])
            break
    
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            D_ft.append(float(lines[0]))
            
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            SEL_dB.append(float(lines[1]))
            
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            LAMAX_dB.append(float(lines[5]))
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(D_ft, SEL_dB, 'o-', D_ft, LAMAX_dB, 'x-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + AC_ENG_PWR_SPEED[0] + "}$" + '\n' + AC_ENG_PWR_SPEED[1]]  # Plot title
    plot_title_2 = [AC_ENG_PWR_SPEED[2] + '\n' + AC_ENG_PWR_SPEED[3]]
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
    #h1,l1 = plt.legend_elements() #legend
    leg = ax.legend(['SEL', 'LAMAX'], fontsize=8)
    leg.set_title("Noise metric",prop={'size':8})
    leg.get_frame().set_edgecolor('black')
    ax.fill_between(D_ft, SEL_dB, LAMAX_dB)
    
    # isDir = os.path.isdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0]) #check if aircraft directory exists
    # if isDir == False: # if aircraft directory does not exist, make it
    #     os.mkdir('./Plots/Flight/' + AC_ENG_PWR_SPEED[0])

def plot_filled(path, file, path_2, file_2):  
    
    AC_ENG_PWR_SPEED = []  #Aircraft name, engine, and power setting from .csv file
    data_path = path # Directory where data is stored
    data_file = file # File name
    D_ft = [] #Slant distance
    SEL_dB = [] #A-G SEL/LAMAX
    LAMAX_dB = []
    
    AC_ENG_PWR_SPEED_2 = []  #Aircraft name, engine, and power setting from .csv file
    data_path_2 = path_2 # Directory where data is stored
    data_file_2 = file_2 # File name
    D_ft_2 = [] #Slant distance
    SEL_dB_2 = [] #A-G SEL/LAMAX
    LAMAX_dB_2 = []
    
    # The following block of code populates the AC_ENG_PWR_SPEED list
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        for lines in csv_reader:
            AC_ENG_PWR_SPEED.append(lines[0])
            AC_ENG_PWR_SPEED.append(lines[1])
            AC_ENG_PWR_SPEED.append(lines[2])
            AC_ENG_PWR_SPEED.append(lines[3])
            break
    
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            D_ft.append(float(lines[0]))
            
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            SEL_dB.append(float(lines[1]))
            
    with open(data_path+data_file) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            LAMAX_dB.append(float(lines[5]))
            
    with open(data_path_2+data_file_2) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        for lines in csv_reader:
            AC_ENG_PWR_SPEED_2.append(lines[0])
            AC_ENG_PWR_SPEED_2.append(lines[1])
            AC_ENG_PWR_SPEED_2.append(lines[2])
            AC_ENG_PWR_SPEED_2.append(lines[3])
            break
    
    with open(data_path_2+data_file_2) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            D_ft_2.append(float(lines[0]))
            
    with open(data_path_2+data_file_2) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            SEL_dB_2.append(float(lines[1]))
            
    with open(data_path_2+data_file_2) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)
        for lines in csv_reader:
            LAMAX_dB_2.append(float(lines[5]))
                
    fig, ax = plt.subplots() # Create aplot
    plt.plot(D_ft, SEL_dB, '-', D_ft, LAMAX_dB, '-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plt.plot(D_ft_2, SEL_dB_2, 'C0-', D_ft_2, LAMAX_dB_2, 'C1-', linewidth=0.7, markerfacecolor='none', markeredgewidth=0.7, ms=4)
    plot_title = [r"$\bf{" + AC_ENG_PWR_SPEED[0] + "}$" + '\n' + AC_ENG_PWR_SPEED[1]]  # Plot title
    plot_title_2 = [Description + ' (' + Range + ')' + '\n' + AC_ENG_PWR_SPEED[3]]
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
    ax.fill_between(D_ft, SEL_dB, SEL_dB_2, alpha=0.5, zorder=3)
    ax.fill_between(D_ft, LAMAX_dB, LAMAX_dB_2, alpha=0.5, zorder=2)
    
    if Save == 1:
            plt.savefig(data_path+AC_ENG_PWR_SPEED[0]+'_range'+'.png', bbox_inches='tight', dpi=1000)


def plot_all():
    Name_list = os.listdir(Directory)
    for filename in Name_list:
        AC_NAME = [] #Get the name of the current aircraft to add it to the Destination variable
        with open(Directory+filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for lines in csv_reader:
                AC_NAME.append(lines[0])
                break
        
        plot_line(Directory, filename) 
        print(filename)
        Destination = Directory+filename[:-4]+'.png'
        print(Destination)
        if Save == 1:
            plt.savefig(Destination, bbox_inches='tight', dpi=1000)
                
plot_filled('C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/', 'A3_J57-P-10_90RPM.csv', 'C:/Users/AESO 1/Documents/Noise/Omega10_2-2-20/data/', 'A3_J57-P-10_95RPM.csv')
