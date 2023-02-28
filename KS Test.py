# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:01:43 2023

@author: rhbjo
"""

from data_handler import *
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import copy

path = 'G:/My Drive/Physics Project/messier 23-filtered.json'
filtered_data = Data(path)

paralexes = filtered_data.get_parallax()

Test = stats.kstest(np.linspace(1/len(paralexes),1, len(paralexes)), stats.uniform.cdf)
print(Test)
