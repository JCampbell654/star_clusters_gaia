# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:25:21 2023

@author: rhbjo
"""

#%% Functions
from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from scipy import stats
import copy

#%% Importing Data
data_folder = 'C:/Users/rhbjo/OneDrive - The University of Nottingham/Shared/'
data = Data(data_folder + 'Messier 47-kstest-filtered.json')

pmr, pmt = data.change_basis()

def cal_cumfreq(key, velocity):
    numbins=100
    x = np.linspace(velocity.min(), velocity.max(), numbins)
    sigma = np.std(velocity)
    mu = np.mean(velocity)
    
    fig, ax = plt.subplots()
    
    cumfreq, x, _ = plt.hist(velocity, bins=numbins, density=True, cumulative=True)
    
    dx = x[1]-x[0]
    y = ((1/(np.sqrt(2*np.pi) * sigma)))*np.exp(-(1/2)*((x-mu)/sigma)**2)
    y = np.cumsum(y)*dx
    
    #plotting
    plt.plot(x, y, lw=2, c='r')
    ax.set_xlabel(f'{key} velocity')
    ax.set_ylabel('cumfreq density')
    plt.show()
    
    
    return cumfreq

#%%ks-test

def ks_test(key, velocity):
    cumfreq = cal_cumfreq(key, velocity)
    ks_test = stats.ks_1samp(cumfreq, stats.norm.cdf)
    p_val = ks_test.pvalue
    print(p_val)

ks_test('pmr', pmr)
ks_test('pmt', pmt)



