from data_handler import *
import matplotlib.pyplot as plt
import numpy as np

#Initialize data
data = Data("Filtered Data/Messier 47-kstest-filtered.json")
pmr, pmt = data.change_basis()

#Initialize x-axis and gaussian parameters
bins=100
x = np.linspace(pmr.min(), pmr.max(), bins)
sigma = np.std(pmr)
mu = np.mean(pmr)

#Plot historgram
y, x, _ = plt.hist(pmr, bins=bins, density=True, cumulative=True)

#Calculate cumulative gaussian
dx = x[1]-x[0]
y = ((1/(np.sqrt(2*np.pi) * sigma)))*np.exp(-(1/2)*((x-mu)/sigma)**2)
y = np.cumsum(y)*dx

#Plot
plt.plot(x, y)
plt.show()


