import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy import stats
from scipy import optimize as opt
import matplotlib.pyplot as plt

lag_h = 6
fitting_range = 50
selected_model = 3

source_arr = np.genfromtxt("source.csv", delimiter=",", skip_header=1)
print(source_arr[:, 2:3])
def variogram(xyv_array):
    xy_dist = pdist(xyv_array[:,0:2], "euclidean")
    s_vario = pdist(xyv_array[:,2:3], "euclidean")**2 / 2
    return [xy_dist, s_vario]

z_vario = variogram(source_arr)

def emp_variogram(z_vario, lag_h):
    num_rank = int(np.max(z_vario[0]) / lag_h)
    bin_means, bin_edges, bin_number = stats.binned_statistic(z_vario[0], z_vario[1], statistic="mean", bins=num_rank)
    bin_centers = np.array([(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(bin_edges)-1)])
    e_vario = np.stack([bin_centers, bin_means], axis=0)
    #e_vario = np.stack([bin_edges[1:], bin_means[0:]], axis=0)
    e_vario = np.delete(e_vario, np.where(e_vario[1] <= 0)[0], axis=1)
    return e_vario

e_vario = emp_variogram(z_vario, 6)

def linear_model(x, a, b):
    return a + b * x
def gaussian_model(x, a, b, c):
    return a + b * (1 - np.exp(-(x / c)**2))
def exponential_model(x, a, b, c):
    return a + b * (1 - np.exp(-(x / c)))
def spherical_model(x, a, b, c):
    cond = [x < c, x > c]
    func = [lambda x : a + (b / 2) * (3 * (x / c) - (x / c)**3), lambda x : a + b]
    return np.piecewise(x, cond, func)

def auto_fit(e_vario, fitting_range, selected_model):
    data = np.delete(e_vario, np.where(e_vario[0]>fitting_range)[0], axis=1)
    if (selected_model == 0):
        param, cov = opt.curve_fit(linear_model, data[0], data[1])
    elif (selected_model == 1):
        param, cov = opt.curve_fit(gaussian_model, data[0], data[1], [0, 0, fitting_range])
    elif (selected_model == 2):
        param, cov = opt.curve_fit(exponential_model, data[0], data[1], [0, 0, fitting_range])
    else:
        param, cov = opt.curve_fit(spherical_model, data[0], data[1], [0, 0, fitting_range])
    return param

def gamma_func(x, param, selected_model):
    if selected_model == 0:
        return linear_model(x, param[2], param[3])
    elif selected_model == 1:
        return gaussian_model(x, param[2], param[3], param[4])
    elif selected_model == 2:
        return exponential_model(x, param[2], param[3], param[4])
    else:
        return spherical_model(x, param[2], param[3], param[4])

param = auto_fit(e_vario, fitting_range, selected_model)
param = np.insert(param, 0, fitting_range)
param = np.insert(param, 0, selected_model)
"""
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(e_vario[0], e_vario[1], "o")
xlim_arr = np.arange(0, np.max(e_vario[0]), lag_h)

if param[0] == 0:
    ax.plot(xlim_arr, linear_model(xlim_arr, param[2], param[3]))
    print(param[2], param[3])
elif param[0] == 1:
    ax.plot(xlim_arr, gaussian_model(xlim_arr, param[2], param[3], param[4]))
    print(param[2], param[3], param[4])
elif param[0] == 2:
    ax.plot(xlim_arr, exponential_model(xlim_arr, param[2], param[3], param[4]))
    print(param[2], param[3], param[4])
else:
    ax.plot(xlim_arr, spherical_model(xlim_arr, param[2], param[3], param[4]))
    print(param[2], param[3], param[4])

ax.set_title("Semivariogram")
ax.set_xlim([0, np.max(e_vario[0])])
ax.set_ylim([0, np.max(e_vario[1])])
ax.set_xlabel("Distance [m]")
ax.set_ylabel("Semivariance")

aspect = 0.8 * (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
ax.set_aspect(aspect)

plt.show()
"""
def solve(x0, xyv_array, param, selected_model):
    pd = pdist(xyv_array[:, 0:2], "euclidean")
    sq = squareform(pd)
    A = gamma_func(sq, param, selected_model)
    A = np.vstack((A, np.ones(A.shape[1])))
    A = np.hstack((A, np.ones((A.shape[0], 1))))
    A[-1][-1] = 0
    b = np.hstack((np.sqrt(np.sum((xyv_array[:, 0:2] - x0)**2, axis=1)), [1]))
    return np.linalg.solve(A, b)

w_list = solve([30, 30], source_arr, param, selected_model)

def kriging(w_list, xyv_array):
    return np.sum(w_list[:-1] * xyv_array[:, 2])

print(kriging(w_list, source_arr))