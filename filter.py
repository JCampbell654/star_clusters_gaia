from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson


def none_filter(data):

	#Exclude all data that has "None" for any of the necessary measurements
	p = data.get_parallax()
	p = (p != None)
	data.data = data.data[p, :]
	return data

def parallax_probability_distribution(position, uncertainty):
	x = np.linspace(position-uncertainty, position+uncertainty, 100)
	y = (x/x)/(2*uncertainty)
	return x, y

def parallax_filter(data, distance, radius):

	#Get parallax data
	p = data.get_parallax() * 1e-3
	p_err = data.get_parallax_err() * 1e-3

	#Calculate distances from parallax data
	star_dist = 1/p
	star_dist_err = np.abs(p_err/(p**2))

	#Find limits for possible cluster region
	x_l = distance - radius
	x_u = distance + radius
	
	probability = np.array([])

	for i in range(star_dist.size):
		x_pd, y_pd = parallax_probability_distribution(star_dist[i], star_dist_err[i])
		_filter = np.logical_and((x_pd > x_l), (x_pd < x_u))
		x_pd = x_pd[_filter]
		y_pd = y_pd[_filter]

		if x_pd.size == 0:
			probability = np.append(probability, 0)
		else:
			dx = (x_pd.max() - x_pd.min()) / x_pd.size
			#Calculate area under curve
			probability = np.append(probability, simpson(y_pd, dx=dx))

	return probability


