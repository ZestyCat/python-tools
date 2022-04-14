# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 14:31:20 2022

@author: AESO 1
"""

# Calculates the distance between two points using the Haversine formula

from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

print(distance(32.712256, -117.211899, 32.70941, -117.21193)*3280.8399)