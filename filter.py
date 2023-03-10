from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from scipy import stats
import copy


def segments_intersect(x1, x2, y1, y2):
    # Assumes x1 <= x2 and y1 <= y2; if this assumption is not safe, the code
    # can be changed to have x1 being min(x1, x2) and x2 being max(x1, x2) and
    # similarly for the ys.
    return np.logical_and(x2 >= y1, y2 >= x1)

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
	#y = (x/x)/(2*uncertainty)
	#Normalised gaussian distribution
	y = ((1/(2*np.pi*uncertainty))**(1/2))*np.exp(-((x-position)**2)/(2*uncertainty))
	return x, y

def parallax_filter(data, distance, radius):

	#Get parallax data
	par = data.get_parallax() * 1e-3
	par_err = data.get_parallax_err() * 1e-3

	#Calculate distances from parallax data
	star_dist = 1/par
	star_dist_err = np.abs(par_err/(par**2))

	#Find limits for possible cluster region
	cluster_limit_l = distance - radius
	cluster_limit_u = distance + radius

	#Check if cluster range intersects uncertainty
	_filter = segments_intersect(cluster_limit_l, cluster_limit_u, star_dist - star_dist_err, star_dist + star_dist_err)

	#Check if parallax uncertainty is too large (discard if it is)
	probability = np.logical_and(_filter, star_dist > star_dist_err*3).astype(int)
	
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
		
		pc = plt.pcolormesh(x_d, y_d, density)
		sc = plt.scatter(filtered_pmra, filtered_pmdec, s=1, c=weighted_probability, cmap=plt.cm.hot)
		plt.colorbar(sc, label="Membership probability")

		plt.show()

	return filtered_data, weighted_probability

def select_data(data, probability, acceptance_value):

	#Filter all stars that are below acceptance value
	_filter = (probability >= acceptance_value)
	copy_data = copy.copy(data)
	copy_data.data = copy_data.data[_filter, :]

	return copy_data
