from data_handler import *
import numpy as np
import matplotlib.pyplot as plt

raw_data = Data("Data/1676314285780O-result.json")

fig, (ax_raw, ax_f) = plt.subplots(1, 2)
ax_raw.scatter(raw_data.get_pmra(), raw_data.get_pmdec(), 1)
ax_raw.set_title("Unfiltered data")
ax_raw.set_xlabel("Proper motion right ascension [mas.yr**-1]")
ax_raw.set_ylabel("Proper motion declination [mas.yr**-1]")

def line_intersect(x1, x2, y1, y2):
	return x2 >= y1 and y2 >= x1

def none_filter(data):

	#Exclude all data that has "None" for any of the necessary measurements
	p = data.get_parallax()
	p = (p != None)
	data.data = data.data[p, :]
	return data

def parallax_filter(data, cluster_distance, cluster_radius):

	star_distance = 1/(data.get_parallax()*1e-3)
	star_distance_err = 1/(data.get_parallax_err()*1e-3)

	x1 = cluster_distance - cluster_radius
	x2 = cluster_distance + cluster_radius
	y1 = star_distance - (star_distance_err / 2)
	y2 = star_distance + (star_distance_err / 2)
	#filter_arr = np.where(line_intersect(x1, y1, x2, y2), True, False)
	a = x2 >= y1
	b = y2 >= x1
	c = np.array([], dtype=bool)
	for i in range(len(a)):
		if (a[i] == True and b[i] == True):
			c = np.append(c, True)
		else:
			c = np.append(c, False)

	data.data = data.data[c, :]

parallax_filter(none_filter(raw_data), 325, 4.59902)

ax_f.scatter(raw_data.get_pmra(), raw_data.get_pmdec(), 1)
ax_f.set_title("Filtered data")
ax_f.set_xlabel("Proper motion right ascension [mas.yr**-1]")
ax_f.set_ylabel("Proper motion declination [mas.yr**-1]")

plt.show()
