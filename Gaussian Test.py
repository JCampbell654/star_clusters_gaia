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
data_folder = 'C:/Users/rhbjo/OneDrive - The University of Nottingham/Shared/Filtered Data/'
data = Data(data_folder + 'Messier 47-kstest-filtered.json')

pmr, pmt = data.change_basis()

#%%

def exclude_tails(n, velocity):
    sorted_data = np.sort(velocity)
    excluded_tails = sorted_data[n:-n]
    
    return excluded_tails

#%%
def cal_cumfreq(key, velocity):
    numbins=100
    x = np.linspace(velocity.min(), velocity.max(), numbins)
    sigma = np.std(velocity)
    mu = np.mean(velocity)
    
    fig, ax = plt.subplots()
    
    bar_heights, x, _ = plt.hist(velocity, bins=numbins, density=True, cumulative=True)
    
    y = stats.norm.cdf(x, mu, sigma)
    
    #plotting
    plt.plot(x, y, lw=2, c='r')
    ax.set_xlabel(f'{key} velocity')
    ax.set_ylabel('cumfreq density')
    plt.show()
        
    return bar_heights, mu, sigma

#%%ks-test

def ks_test(key, velocity):
    cumfreq, mu, sigma = cal_cumfreq(key, velocity)
    ks_test = stats.ks_1samp(cumfreq, stats.norm.cdf, args=(mu, sigma))
    test_statistic = ks_test.statistic
    p_val = ks_test.pvalue
    print(test_statistic, p_val)

ks_test('pmr', pmr)
ks_test('pmt', pmt)



