import json
import numpy as np

file_path = "";

global data, metadata
data = np.zeros([])
metadata = np.zeros([])

#Select a data file
def select_file(path):
	global data, metadata
	file_path = open(path)
	content = json.load(file_path)

	data = np.array(content['data'])
	metadata = np.array(content['metadata'])

def get_metadata_index(key):
	global metadata

	size = metadata.size
	for i in range(size):
		if (metadata[i]['name'] == key):
			return i

def get_ra():
	metadata_key = "ra"
	index = get_metadata_index(metadata_key)
	return data[:, index]
	
def get_dec():
	metadata_key = "dec"
	index = get_metadata_index(metadata_key)
	return data[:, index]

def get_pmra():
	metadata_key = "pmra"
	index = get_metadata_index(metadata_key)
	return data[:, index]

def get_pmdec():
	metadata_key = "pmdec"
	index = get_metadata_index(metadata_key)
	return data[:, index]

def get_parallax():
	metadata_key = "parallax"
	index = get_metadata_index(metadata_key)
	return data[:, index]

def get_star_data(index):
	global data
	return data[index, :]
