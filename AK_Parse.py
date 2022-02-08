# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 15:03:50 2022

@author: AESO 1
"""

import csv

path = 'C:/Users/AESO 1/Documents/THC Analyzer/akprotocol test/' # Directory
data_file = 'test1.txt' # Data file name
output_file = 'output.csv' # Output file name

f = open(path + data_file)
text = f.read()

ind = [i for i in range(len(text)) if text.startswith('_AKON 2', i)] # Indexes of measurements in data file

data = []

for i in ind:
    try:
        data.append(float(text[i+8:i+18]))
    except:
        print('could not convert to float')

with open(path + output_file, 'w') as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['Measurement', 'Concentration'])
    for i, d in enumerate(data):
        writer.writerow([i, d])