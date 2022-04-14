# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:57:30 2022

@author: AESO 1
"""

# What percent of the noise data in flight01.dat is estimated?

Meas = 0
Est = 0

with open('C:/Noisemap/NMap/flight01.dat') as file:
    for i, line in enumerate(file):
        if (i + 4) % 5 == 0: # Get the second out of every fifth line
            if "MEASURED" in line:
                Meas += 1
            if "ESTIMATED" in line:
                Est += 1
                
Est_pct = 100 * (Est / Meas)

print(Est_pct)

# Expected output: 15.275994865211809