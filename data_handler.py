import json
import numpy as np

class Data:
	def __init__(self, path):
		content = json.load(open(path))
		self.data = np.array(content['data'])
		self.metadata = np.array(content['metadata'])


	def get_metadata_index(self, key):
		size = self.metadata.size
		for i in range(size):
			if (self.metadata[i]['name'] == key):
				return i

	def save(self, path):
		data = self.data.tolist()
		metadata = self.metadata.tolist()
		final_data = {"metadata": metadata, "data": data}
		with open(path, "w") as outfile:
			outfile.write(json.dumps(final_data))

	@property
	def ra(self):
		metadata_key = "ra"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@ra.setter
	def ra(self, value):
		metadata_key = "ra"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value
		
	@property
	def dec(self):
		metadata_key = "dec"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@dec.setter
	def dec(self, value):
		metadata_key = "dec"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value

	@property
	def pmra(self):
		metadata_key = "pmra"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@pmra.setter
	def pmra(self, value):
		metadata_key = "pmra"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value

	@property
	def pmdec(self):
		metadata_key = "pmdec"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@pmdec.setter
	def pmdec(self, value):
		metadata_key = "pmdec"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value

	@property
	def parallax(self):
		metadata_key = "parallax"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@property
	def parallax_err(self):
		metadata_key = "parallax_error"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@property
	def pmr(self):
		metadata_key = "pmr"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@pmr.setter
	def pmr(self, value):
		metadata_key = "pmr"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value

	@property
	def pmt(self):
		metadata_key = "pmt"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index].astype(float)

	@pmt.setter
	def pmt(self, value):
		metadata_key = "pmt"
		index = self.get_metadata_index(metadata_key)
		self.data[:, index] = value

	def get_data_size(self):
		return self.data.shape[0]

	def centralize_proper_motion(self):
		#Get data
		y_data = self.pmdec
		x_data = self.pmra

		#Calculate mean velocities of stars
		x_avg = np.mean(x_data)
		y_avg = np.mean(y_data)

		#Adjust all velocities accordingly to reference frame of cluster
		x_data = x_data - x_avg
		y_data = y_data - y_avg

		self.pmra = x_data
		self.pmdec = y_data

	def centralize_position(self):
		
		#Get data
		y_data = self.dec
		x_data = self.ra

		#Calculate mean velocities of stars
		x_avg = np.mean(x_data)
		y_avg = np.mean(y_data)

		#Adjust all velocities accordingly to reference frame of cluster
		x_data = x_data - x_avg
		y_data = y_data - y_avg

		self.ra = x_data
		self.dec = y_data

	def change_basis(self): # Function to change pmra and pmdec into pm in the angular ditection and pm in radial direction

	    ra = self.ra
	    dec = self.dec
	    pmra = self.pmra
	    pmdec = self.pmdec

	    theta = np.arctan(list(dec/ra))

	    pmtheta = pmdec*np.cos(theta) - pmra*np.sin(theta)
	    pmr = pmdec*np.sin(theta) + pmra*np.cos(theta)

	    return pmr, pmtheta
