from data_handler import *
from anisotropy_parameter import *
import matplotlib.pyplot as plt

data = Data("Filtered Data/messier 67-filtered.json")

x, y = centralize_position(data)
dist = np.sqrt(x.astype(float)**2+y.astype(float)**2)
min_r = np.min(dist)
max_r = np.max(dist)

rad = np.linspace(min_r+0.1, max_r, 10)
ap_arr = np.array([])
err_arr = np.array([])

for r in rad:
	r_data = points_in_radius(data, r)
	ap = anisotropy_parameter(r_data)
	ap_arr = np.append(ap_arr, ap)
	err = 2*(1-ap)*(1/(r_data.get_data_size()-1)**(1/2))
	err_arr = np.append(err_arr, err)

plt.ylim([-2, 1])
plt.errorbar(rad, ap_arr, err_arr)
plt.show()
