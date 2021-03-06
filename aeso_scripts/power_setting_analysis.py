# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 08:27:09 2022

Uses linear interpolation to generate a new data file which can be plotted by Noise_Slant_Line.py

@author: Gregory Bizup (gregory.bizup@compass-sys-inc.com, 240-587-9468)
"""

''' User input section'''

search_string = 'AV-8B_F402-RR-405' # Phrase to search for in directory
search_directory = './data/csv/Flight/' # Directory to look for search string
aircraft_name = 'AV-8B' # Name of the aircraft
power_units = ' % RPM' # Units used for power setting
power_description = 'Cruise'
interpolate = '89' # Power setting where SEL should be calculated through linear interpolation.

write_directory = './data/'
writefile = 'y'
write_filename = 'AV-8B-89RPM_interpolation.csv' # Name of new power setting file to write. It is saved into the search directory

plot = 'y' # plot the derived values? 'y' for yes
just_plot = 'n' # set to 'y' to just plot and not add red dot with new values
save = 'y' # save figure? y for yes
save_directory = './data/'
savename = 'C-5A_example' # name to save figure as

''' End user input section'''


'''Module imports'''
import os
import csv
import re
import matplotlib.pyplot as plt

'''Variable declaration'''
distance_ft = [] # Distance from aircraft in ft, string
SEL_new = [] # New SEL values to be exported to csv files
LMAX_new = [] # New LMAX values to be exported to csv files
engine = [] #aircraft engine

files = os.listdir(search_directory)
for file in files:
    if search_string in file:
        with open(search_directory + file) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            next(reader)
            next(reader)
            for row in reader:
                distance_ft.append(row[0])
            break

'''Interpolation function'''
def interpolation(distance): # Interpolate at given distance
    description = [] # Power setting description string
    power = [] # Power setting float
    SEL_dB = [] #sound exposure level in db
    LMAX_dB = [] # LMAX in dB
    SEL_dB_interp = [] # SEL calculated through interpolation
    LMAX_dB_interp = [] # LMAX calculated through interpolation

    for file in files: # for every file
        if search_string in file: # if file contains search string
            with open(search_directory + '/' + file) as csvfile: #open that file
                reader = csv.reader(csvfile) # make a reader object
                i = 0  # set iteration count to zero
                power_setting = [] # make empty array for power settings
                for row in reader:
                    if i == 0: # if we are on the first row
                        power_setting.append(row[2]) #get the power setting info
                        engine.append(row[1])
                        i +=1  #set i to 1
                    if row[0] == distance: # if we are on the row matching the distance parameter
                        description.append(power_setting[0]) # append power description
                        SEL_dB.append(float(row[1])) #a append SEL
                        LMAX_dB.append(float(row[5]))

    for d in description:
        number = re.findall('[\d|\.]+', d) # search for decimal number in power setting string. possible error source as regex may need to change depending on input file
        power.append(float(number[0])) # turn that number into a float and put it in the power array

    if interpolate != 'n': # linear interpolation

        x = float(interpolate)

        gt_list = [] # all power numbers greater than x and list index
        lt_list = [] # all power numbers less than x and list index

        i = 0
        for p in power:
            if p > x:
                gt_list.append([i, p])
            if p < x:
                lt_list.append([i, p])
            if p == x:
                gt_list.append([i, p])
            i +=1

        gt_list = sorted(gt_list, key = lambda l:l[1]) #Sorts by, you know, the power setting itself
        lt_list = sorted(lt_list, key = lambda l:l[1]) #Sorts by, you know, the power setting itself

        x1 = lt_list[-1][1]
        x2 = gt_list[0][1]
        y1_sel = SEL_dB[lt_list[-1][0]]
        y2_sel = SEL_dB[gt_list[0][0]]
        y1_lmax = LMAX_dB[lt_list[-1][0]]
        y2_lmax = LMAX_dB[gt_list[0][0]]

        m_sel = (y2_sel - y1_sel)/(x2 - x1) # derive slope for interpolation
        y_sel = m_sel * (x - x1) + y1_sel # solve for y
        SEL_dB_interp.append(y_sel)
        SEL_new.append(y_sel)

        m_lmax = (y2_lmax - y1_lmax)/(x2 - x1) # derive slope for interpolation
        y_lmax = m_lmax * (x - x1) + y1_lmax #solve for y
        LMAX_dB_interp.append(y_lmax)
        LMAX_new.append(y_lmax)

    new_xs, new_ys = zip(*sorted(zip(power, SEL_dB))) #sort by increasing x value
    new_xl, new_yl = zip(*sorted(zip(power, LMAX_dB)))

    if plot == 'y':
        fig, ax = plt.subplots() #plot
        ax.plot(new_xs, new_ys, marker='o', linestyle='-')
        ax.plot(new_xl, new_yl, marker='o', linestyle='-')
        plt.title(aircraft_name + ' power setting vs SEL and LMAX\n at ' + distance + 'ft. slant distance')
        plt.xlabel('Engine power setting in ' + power_units)
        plt.ylabel('Noise level (dB)')
        if just_plot != 'y':
            ax.plot(float(interpolate), SEL_dB_interp, 'ro')
            ax.plot(float(interpolate), LMAX_dB_interp, 'ro')
            plt.annotate('   SEL = ' + str(round(SEL_dB_interp[0], 2)) + ' dB', xy = (float(interpolate), SEL_dB_interp[0]))
            plt.annotate('   LMAX = ' + str(round(LMAX_dB_interp[0], 2)) + ' dB', xy = (float(interpolate), LMAX_dB_interp[0]))

'''Write new datafile function'''
def write(aircraft, engine, description, units, powersetting, distance, SEL, LMAX): # Write data file in format taken by Noise_Slant_Line.py
    with open(write_directory+write_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator = '\n')

        rows = [[aircraft, engine, description + ' (' + powersetting + power_units + ')', '160kts'],
                   ['Distance', 'SEL','n/a','n/a','n/a','LMAX'],
                   ['(ft)', 'A-G']]

        csvwriter.writerows(rows)
        i = 0
        for d in distance:
            csvwriter.writerow([d, SEL[i],'n/a','n/a','n/a',LMAX[i]])
            i += 1

'''Function calls'''
fig = 0
for d in distance_ft:
    interpolation(d)
    if save == 'y' and plot == 'y':
        plt.savefig(save_directory+savename+str(fig)+'.png', dpi=1000)
        fig += 1

if writefile == 'y':
    write(aircraft_name, engine[0], power_description, power_units, interpolate, distance_ft, SEL_new, LMAX_new)
