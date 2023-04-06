from data_handler import *
from filter import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

path = "Data/NGC 5460.json"

distance_range = (0, 2000)

data = Data(path)
dist = 1/(data.parallax * 1e-3)
data.data = data.data[np.logical_and(dist > distance_range[0], dist < distance_range[1]), :]
centre = np.array([-6.64, -3.36])

dist = np.sqrt((data.pmra-centre[0])**2 + (data.pmdec-centre[1])**2)
data.data = data.data[dist < 1, :]

plt.xlabel("Distance [pc]")
plt.ylabel("Number of stars")
y, x, _ = plt.hist(1/(data.parallax * 1e-3), bins=200)
_x = np.zeros(y.size)

#Find points of half maximum
_max = y.max()
bounds = np.array([_max, _max])
x_bounds = np.array([0, 0])

i = np.where(y == y.max())[0]
while bounds[0] >= _max/2:
	i -= 1
	bounds[0] = y[i]
x_bounds[0] = x[i]

i = np.where(y == y.max())[0]
while bounds[1] >= _max/2:
	i += 1
	bounds[1] = y[i]
x_bounds[1] = x[i]

radius = x_bounds[1]-x_bounds[0]
distance = x[np.where(y == y.max())][0]

plt.show()

data = Data(path)
filtered_data, probability = filter_data(data, distance, radius, plot=True)
selected_data = select_data(filtered_data, probability, 0.9)
print(selected_data.get_data_size())
