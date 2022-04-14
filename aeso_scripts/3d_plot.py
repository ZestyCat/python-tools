# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 10:08:07 2022

@author: AESO 1
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import re
import matplotlib.cm as cm

search_string = 'U-6' # Phrase to search for in directory
search_directory = 'C:/Users/AESO 1/Documents/Noise/csv/Flight/' # Directory to look for search string
aircraft_name = 'U-6' # Name of the aircraft
power_units = '% ETR' # Units used for power setting
power_description = 'Cruise'
interpolate = '92' # Power setting where SEL should be calculated through linear interpolation. 
writefile = 'y'
write_filename = 'F-35B_Custom_Power_Setting.csv' # Name of new power setting file to write. It is saved into the search directory
just_plot = 'y' # set to 'y' to just plot and not interpolate

files = os.listdir(search_directory) # List files in directory

distance_ft = [] # Distance from aircraft in ft, string
description = []
SEL = [] # New SEL values to be exported to csv files
LMAX = [] # New LMAX values to be exported to csv files
power = []

for file in files: #makes list of distances 
    if search_string in file:
        with open(search_directory + file) as csvfile:
            reader = csv.reader(csvfile)
            i = 0
            SEL_ps = []
            for row in reader:
                if i == 0:
                    description.append(row[2])
                    i += 1
                elif i < 3:
                    i += 1
                    continue
                else:
                    if len(distance_ft) < 22:
                        distance_ft.append(float(row[0]))
                    SEL_ps.append(float(row[1]))
                    LMAX.append(float(row[5]))
                    i += 1
            SEL.append(SEL_ps)
          
for d in description:
    number = re.findall('[\d|\.]+', d) # search for decimal number in power setting string #Regex may need to change depending on input file
    power.append(float(number[0])) # turn that number into a float and put it in the power array
   
sorted_lists = sorted(zip(power, SEL))
unzipped_lists = list(zip(*sorted_lists))

power_sorted = (list(unzipped_lists[0]))
SEL_sorted = (list(unzipped_lists[1]))

X, Y = np.meshgrid(distance_ft, power_sorted)
SEL_array = np.array(SEL_sorted) 

maxtick = round(SEL_sorted[-1][0], -1) 
mintick = round(SEL_sorted[0][-1], -1)
print(mintick)

zticks = np.linspace(mintick, maxtick, 11)
print(zticks)

fig = plt.figure(figsize=(15,10))
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, SEL_array, cmap='twilight_shifted' )
ax.set_xlabel('Distance (ft.)')
ax.set_ylabel('Power setting (% ETR)')
ax.set_zlabel('SEL (dB)')
ax.set_zticks(zticks)
plt.title("Distance and Power setting vs. SEL for " + aircraft_name, size=22, y=0.95)
m = cm.ScalarMappable(cmap=cm.twilight_shifted)
m.set_array(SEL_array)
cbar = plt.colorbar(m, shrink=0.75, ticks=zticks)
ax.view_init(10, -60)
#plt.savefig('C:/Users/AESO 1/Documents/Noise/Plots/Custom/F35-3D.png', dpi=1000)
plt.show()
