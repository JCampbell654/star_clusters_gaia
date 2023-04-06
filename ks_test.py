# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:25:21 2023

@author: rhbjo
"""

#%% Functions

from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

#%%Files and Folders

cluster = 'NGC 5460'

data_folder = 'C:/Users/rhbjo/OneDrive - The University of Nottingham/Shared/Final Data/'
data = Data(data_folder + f'{cluster}-final.json')

plot_folder = 'C:/Users/rhbjo/OneDrive - The University of Nottingham/Shared/Cumlative Frequency Graphs/'
ks_test_folder = 'C:/Users/rhbjo/OneDrive - The University of Nottingham/Shared/KS Test Data/'

save = False

#%%Cumfreq calculations

pmr, pmt = data.change_basis()

def cal_cumfreq(cluster, key, velocity):
    numbins=100

    sigma = np.std(velocity)
    mu = np.mean(velocity)
    
    x = np.linspace(velocity.min(), velocity.max(), numbins)
    
    fig, ax = plt.subplots()
    
    bar_heights, x, _ = plt.hist(velocity, bins=numbins, density=True, cumulative=True, label='Velocity dist')
    
    y = stats.norm.cdf(x, mu, sigma) # creating normal distribution
    
    #plotting normal distribution
    plt.plot(x, y, lw=2, c='r', label='Normal dist')
    ax.set_xlabel(f'{key} velocity')
    ax.set_ylabel('cumfreq density')
    ax.legend()
    
    plt.show()
    if save == True:
        plt.savefig(plot_folder + f'{cluster}-{key}.png')
        
    return mu, sigma

#%%ks-test
test_statistics = []
p_values = []

def ks_test(cluster, key, velocity):
    mu, sigma = cal_cumfreq(cluster, key, velocity)
    ks_test = stats.ks_1samp(velocity, stats.norm.cdf, args=(mu, sigma))
   
    test_statistic = ks_test.statistic
    p_value = ks_test.pvalue
    
    print(test_statistic, p_value)
    test_statistics.append(test_statistic)
    p_values.append(p_value)

ks_test(cluster, 'pmr', pmr)
ks_test(cluster, 'pmt', pmt)

#%%Saving KS test results

if save == True:
    d = {'Test Statistic': test_statistics, 'P Value': p_values}
    df = pd.DataFrame(data=d, index=['pmr', 'pmt'])
    df.to_json(ks_test_folder + f'{cluster}-KS-test-result.json')



