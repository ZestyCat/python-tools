# -*- coding: utf-8 -*-
"""
Developed to improve the AESO emission index curve fitting process.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = [0.0296, 0.066, 0.1727, 0.2054] # % Thrust
y = [1.66, 4.93, 10.08, 11.13] # FF / EI
x_title = 'Fuel Flow (kg/s)'
y_title = 'EI NOx (lb/1000lb fuel)'
plot_title = 'Fuel Flow vs EI NOx'
fit = 'log' # linear, log, quadratic, cubic

def linear(t, a, b):
    return a * t + b

def log(t, a, b, c):
    return a * np.log(b * t) + c

def exp(t, a, b, c):
    return a * np.exp(b * t) + c

def quadratic(t, a, b, c):
    return a * t ** 2 + b * t + c

def cubic (t, a, b, c, d):
    return a * t ** 3 + b * t ** 2 + c * t + d

dense_x = np.arange(x[0], x[-1], 0.0001)

if fit == 'linear':
    popt, pcov = curve_fit(linear, x, y)
    fit_linear = linear(np.array(x), *popt)
    
    
    fig, ax = plt.subplots()
    plt.plot(x, y, ls='', marker='o', ms=4, color='black')
    plt.plot(x, fit_linear, color='black', linewidth=1)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(plot_title)
    plt.text(0.03, 10.75, 'y = ' + str(round(popt[0], 3)) + 'x + ' + str(round(popt[1], 3)))

if fit == 'log':
    popt, pcov = curve_fit(log, x, y)
    fit_log = log(np.array(dense_x), *popt)
    
    
    fig, ax = plt.subplots()
    plt.plot(x, y, ls='', marker='o', ms=4, color='black')
    plt.plot(dense_x, fit_log, color='black', linewidth=1)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(plot_title)
    plt.text(0.03, 10.75, 'y = ' + str(round(popt[2], 3)) + 'log('+str(round(popt[1], 3))+'x) + ' + str(round(popt[0], 3)))

if fit == 'quadratic':
    popt, pcov = curve_fit(quadratic, x, y)
    fit_quadratic = quadratic(np.array(dense_x), *popt)
    fig, ax = plt.subplots()
    plt.plot(x, y, ls='', marker='o', ms=4, color='black')
    plt.plot(dense_x, fit_quadratic, color='black', linewidth=1)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(plot_title)
    #plt.text(0.03, 10.75, 'y = ' + str(round(popt[2], 3)) + 'x^2 +'+str(round(popt[1], 3))+'x) + ' + str(round(popt[0], 3)))

         
save_as = 'JT15D-5_TFF-NOx'
#plt.savefig(save_as + '.png', dpi=1000)