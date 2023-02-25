from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from scipy import stats
import copy


def none_filter(data):

	#Exclude all data that has "None" for any of the necessary measurements
	_filter = data.get_parallax()
	_filter = (_filter != None)
	data.data = data.data[_filter, :]
	return data

def range_filter(data, limit_l, limit_u):

	#Exclude data that is outside velocity space range
	pmra = data.get_pmra()
	pmdec = data.get_pmdec()
	_filter = (pmra < limit_u)
	_filter = np.logical_and(_filter, pmra > limit_l)
	_filter = np.logical_and(_filter, pmdec < limit_u)
	_filter = np.logical_and(_filter, pmdec > limit_l)
	data.data = data.data[_filter, :]
	return data

def parallax_probability_distribution(position, uncertainty):
	x = np.linspace(position-uncertainty, position+uncertainty, 500)
	y = (x/x)/(2*uncertainty)
	return x, y

def parallax_filter(data, distance, radius):

	#Get parallax data
	par = data.get_parallax() * 1e-3
	par_err = data.get_parallax_err() * 1e-3

	#Calculate distances from parallax data
	star_dist = 1/par
	star_dist_err = np.abs(par_err/(par**2))

	#Find limits for possible cluster region
	x_l = distance - radius
	x_u = distance + radius
	
	#Initialize probability array
	probability = np.array([])

	#Calculate how much of the probability distribution is within the cluster range for each star
	for i in range(star_dist.size):
		x_pd, y_pd = parallax_probability_distribution(star_dist[i], star_dist_err[i])
		_filter = np.logical_and((x_pd > x_l), (x_pd < x_u))
		x_pd = x_pd[_filter]
		y_pd = y_pd[_filter]

		#Calculate area under probability distribution to get probability of membership
		if x_pd.size == 0:
			probability = np.append(probability, 0)
		else:
			dx = (x_pd.max() - x_pd.min()) / x_pd.size
			#Calculate area under curve
			probability = np.append(probability, simpson(y_pd, dx=dx))

	return probability

def point_density(data_x, data_y, probability, limit_l, limit_u, nbins):
	X, Y = np.mgrid[limit_l:limit_u:nbins*1j, limit_l:limit_u:nbins*1j]
	positions = np.vstack([X.ravel(), Y.ravel()])
	values = np.vstack([data_x, data_y])
	kernel = stats.gaussian_kde(values, weights=probability)
	Z = np.reshape(kernel(positions).T, X.shape)

	return Z, X, Y

def weight_probability_with_density(density, probability, data_x, data_y, limit_l, limit_u, nbins):
	#Locate coordinate of highest density
	max_indexes = np.unravel_index(density.argmax(), density.shape)
	max_x = limit_l + (max_indexes[0]/nbins)*(limit_u-limit_l)
	max_y = limit_l + (max_indexes[1]/nbins)*(limit_u-limit_l)

	#Find bin index for each star
	x_bin = np.floor((data_x-limit_l)/(limit_u-limit_l)*nbins).astype(int)
	y_bin = np.floor((data_y-limit_l)/(limit_u-limit_l)*nbins).astype(int)

	#Weight each probability with the density of the correpsonding bin
	density = density/density.max()
	probability = probability * density[x_bin, y_bin]

	return probability

def filter_data(data, cluster_distance, cluster_radius, pm_limit_lower = -15, pm_limit_upper = 15, bins = 300, plot = False):

	#Filter out useless and out of range data
	filtered_data = range_filter(none_filter(data), pm_limit_lower, pm_limit_upper)
	filtered_pmra = filtered_data.get_pmra().astype(float)
	filtered_pmdec = filtered_data.get_pmdec().astype(float)

	#Calculate probabilities of data using parallax data
	probability = parallax_filter(filtered_data, cluster_distance, cluster_radius)

	#Calculate point density
	density, x_d, y_d = point_density(filtered_pmra, filtered_pmdec, probability, pm_limit_lower, pm_limit_upper, bins)

	#Weight probabilities with point density
	weighted_probability = weight_probability_with_density(density, probability, filtered_pmra, filtered_pmdec, pm_limit_lower, pm_limit_upper, bins)

	#Plot data
	if plot == True:
		plt.xlim([pm_limit_lower, pm_limit_upper])
		plt.ylim([pm_limit_lower, pm_limit_upper])

		plt.xlabel("PMRA [mas.yr**-1]")
		plt.ylabel("PMDEC [mas.yr**-1]")
		
		sc = plt.scatter(filtered_pmra, filtered_pmdec, s=1, c=weighted_probability, cmap=plt.cm.hot)
		plt.colorbar(sc, label="Membership probability")

		plt.show()

	return filtered_data, weighted_probability

def select_data(data, probability, acceptance_value):

	#Filter all stars that are below acceptance value
	_filter = (probability >= acceptance_value)
	data.data = data.data[_filter, :]

	return data

