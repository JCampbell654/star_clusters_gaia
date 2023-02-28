"""
Created on Tue Feb 28 16:15:43 2023

@author: Robert Johson
"""
#%% Functions

from data_handler import *
import numpy as np

#%% Folders and files

folder = 'G:/My Drive/Physics Project/Data/' #change to folder where data is kept
messier_23_data = folder + 'messier 23-filtered.json'
messier_34_data = folder + 'messier 34-filtered.json'
messier_39_data = folder + 'messier 39-filtered.json'
ngc_2232_data = folder + 'NGC 2232-filtered.json'
ngc_5460_data = folder + 'NGC 5460-filtered.json'

#%% Functions

def change_basis(data): # Function to change pmra and pmdec into pm in the angular ditection and pm in radial direction
    ra = Data(data).get_ra()
    dec = Data(data).get_dec()
    pmra = Data(data).get_pmra()
    pmdec = Data(data).get_pmdec()
    
    theta = np.arctan(list(dec/ra))
    
    pmtheta = pmdec*np.cos(theta) - pmra*np.sin(theta)
    pmr = pmdec*np.sin(theta) + pmra*np.cos(theta)
    
    return pmtheta, pmr


def anisotropic_parameter(pmtheta, pmr):
    return  1 - (np.sum(pmtheta**2)/np.sum(pmr**2))

#%% Anisotropic Parameter calculations

messier_23_ap = anisotropic_parameter(change_basis(messier_23_data)[0], change_basis(messier_23_data)[1])
messier_34_ap = anisotropic_parameter(change_basis(messier_34_data)[0], change_basis(messier_34_data)[1])
messier_39_ap = anisotropic_parameter(change_basis(messier_39_data)[0], change_basis(messier_39_data)[1])
ngc_2232_ap = anisotropic_parameter(change_basis(ngc_2232_data)[0], change_basis(ngc_2232_data)[1])
ngc_5460_ap = anisotropic_parameter(change_basis(ngc_5460_data)[0], change_basis(ngc_5460_data)[1])
