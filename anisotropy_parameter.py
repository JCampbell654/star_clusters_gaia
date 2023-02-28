from data_handler import *
import numpy as np

def centralize_proper_motion(data):
	#Get data
	y_data = data.get_pmdec()
	x_data = data.get_pmra()

	#Calculate mean velocities of stars
	x_avg = np.mean(x_data)
	y_avg = np.mean(y_data)

	#Adjust all velocities accordingly to reference frame of cluster
	x_data = x_data - x_avg
	y_data = y_data - y_avg

	#Return positions
	return x_data, y_data

def change_basis(data): # Function to change pmra and pmdec into pm in the angular ditection and pm in radial direction
    ra = data.get_ra()
    dec = data.get_dec()
    pmra, pmdec = centralize_proper_motion(data)
    #pmdec = data.get_pmdec()

    theta = np.arctan(list(dec/ra))

    pmtheta = pmdec*np.cos(theta) - pmra*np.sin(theta)
    pmr = pmdec*np.sin(theta) + pmra*np.cos(theta)

    return pmtheta, pmr

#Calculate the anisotropt parameter of each star
def anisotropic_parameter(data):
	pmtheta, pmr = change_basis(data)
	return  1 - (np.sum(pmtheta**2)/np.sum(pmr**2))
