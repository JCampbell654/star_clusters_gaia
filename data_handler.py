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

	def get_ra(self):
		metadata_key = "ra"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]
		
	def get_dec(self):
		metadata_key = "dec"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]

	def get_pmra(self):
		metadata_key = "pmra"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]

	def get_pmdec(self):
		metadata_key = "pmdec"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]

	def get_parallax(self):
		metadata_key = "parallax"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]

	def get_parallax_err(self):
		metadata_key = "parallax_error"
		index = self.get_metadata_index(metadata_key)
		return self.data[:, index]

	def get_star_data(self, index):
		return self.data[index, :]

	def get_data_size(self):
		return self.data.shape[0]
