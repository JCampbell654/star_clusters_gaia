from data_handler import *
import numpy as np
import matplotlib.pyplot as plt
import copy

def points_in_radius(data, radius):

	copy_data = copy.copy(data)
	copy_data.centralize_position()

	ra = copy_data.ra
	dec = copy_data.dec

	dist = np.sqrt(ra**2 + dec**2)
	_filter = (dist <= radius)
	copy_data.data = copy_data.data[_filter, :]

	return copy_data

#Calculate the anisotropy parameter of each star
def anisotropy_parameter(data, plot=False, bins=20):

	#Centralize the data so the origin is at 0,0
	data.centralize_position()
	data.centralize_proper_motion()

	pmr, pmt = data.change_basis()

	#Plot anisotropy parameter as a function of radius
	if plot == True:
		
		#Get min and max radius
		dist = np.sqrt(data.ra**2 + data.dec**2)
		max_r = dist.max()
		lowest_bin = np.ceil(data.get_data_size()/bins).astype(int)
		min_r = np.partition(dist, lowest_bin)[lowest_bin] #Get the second smallest distance to avoid div by 0 error in the uncertainty calculation
		r = np.linspace(min_r, max_r, bins)
		
		#Initialize arrays
		ap_arr = np.array([])
		err_arr = np.array([])

		#Calculate anisotropy parameter and error for all radii
		for i in r:
			r_data = points_in_radius(data, i)
			r_ap = anisotropy_parameter(r_data, plot=False)
			ap_arr = np.append(ap_arr, r_ap)
			err_arr = np.append(err_arr, 2 * (1-r_ap) * ((1/(r_data.get_data_size()-1))**(1/2)))

		#Plot anisotropy parameter as a function of radius
		plt.xlabel("r/R")
		plt.ylabel(r'$\beta = 1-\sigma_t^2/\sigma_r^2$')
		plt.errorbar(r/max_r, ap_arr, yerr=err_arr)

	#Return value
	return  1 - (np.std(pmt)**2/np.std(pmr)**2), 2 * ((np.std(pmt)**2/np.std(pmr)**2)) * ((1/(data.get_data_size()-1))**(1/2))
