import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy import stats
from scipy.linalg import lu_factor, lu_solve
from scipy import optimize as opt
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from GySon.dataset import load_toyama_second_pos
from GySon.colormap import rb

def semivariogram(xy, v, lag_h=None, fitting_range=None, selected_model=3, plot=False, plot_raw=False):
    z_vario = variogram(xy, v)
    if lag_h == None:
        lag_h = np.max(z_vario[0]) / 10
    if fitting_range == None:
        fitting_range = np.max(z_vario[0]) / 2
    if plot_raw:
        plt.scatter(z_vario[0], z_vario[1])
        plt.show()
    e_vario = emp_variogram(z_vario, lag_h)
    param = auto_fit(e_vario, fitting_range, selected_model)
    param = np.insert(param, 0, fitting_range)
    param = np.insert(param, 0, selected_model)

    if plot:
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
        
    return param, lag_h, fitting_range, selected_model

def variogram(xy, v):
    xy_dist = pdist(xy, "euclidean")
    s_vario = pdist(v.reshape(v.shape[0], 1), "euclidean")**2 / 2
    return [xy_dist, s_vario]

def emp_variogram(z_vario, lag_h):
    num_rank = int(np.max(z_vario[0]) / lag_h)
    bin_means, bin_edges, bin_number = stats.binned_statistic(z_vario[0], z_vario[1], statistic="mean", bins=num_rank)
    bin_centers = np.array([(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(bin_edges)-1)])
    e_vario = np.stack([bin_centers, bin_means], axis=0)
    e_vario = np.delete(e_vario, np.where(e_vario[1] <= 0)[0], axis=1)
    return e_vario

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

def solve(x0, xy, param, selected_model):
    pd = pdist(xy, "euclidean")
    sq = squareform(pd)
    A = gamma_func(sq, param, selected_model)
    A = np.vstack((A, np.ones(A.shape[1])))
    A = np.hstack((A, np.ones((A.shape[0], 1))))
    A[-1][-1] = 0
    b = np.hstack((np.sqrt(np.sum((xy - x0)**2, axis=1)), [1]))
    return np.linalg.solve(A, b)

def kriging(x0, xy, v, param, selected_model):
    w_list = solve(x0, xy, param, selected_model)
    return np.sum(w_list[:-1] * v.reshape(v.shape[0], 1))

def kriging_mtx(xy_lim: list, size: list, xy, v, param, selected_model):
    pd = pdist(xy, "euclidean") # manhattan
    sq = squareform(pd)
    A = gamma_func(sq, param, selected_model)
    A = np.vstack((A, np.ones(A.shape[1])))
    A = np.hstack((A, np.ones((A.shape[0], 1))))
    A[-1][-1] = 0
    LU = lu_factor(A)

    x_arr = np.linspace(xy_lim[0][0], xy_lim[0][1], size[0]*20)
    y_arr = np.linspace(xy_lim[1][0], xy_lim[1][1], size[1]*20)
    krig_mtx = np.zeros((size[1]*20, size[0]*20))

    for i, x in enumerate(x_arr):
        print(i)
        for j, y in enumerate(y_arr):
            b = np.hstack((gamma_func(np.linalg.norm((xy-np.array([x, y])), ord=2, axis=1), param, selected_model), [1]))
            w = lu_solve(LU, b)
            krig_mtx[j][i] = np.sum(w[:-1] * v)
    
    return krig_mtx, x_arr, y_arr

def kriging_plot(dataset, xy, v, param, selected_model, save_name=None, front_color="rb", title=None, show=True):
    fig = plt.figure(figsize=(9,8))
    gs_master = GridSpec(nrows=1, ncols=2, width_ratios=[8, 1])
    gs_1 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 0])
    ax = fig.add_subplot(gs_1[:, :])
    gs_2 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 1])
    ax_c = fig.add_subplot(gs_2[:, :])

    for i in dataset["back"].keys():
        poly = plt.Polygon(dataset["back"][i], fill=False)
        ax.add_patch(poly)

    if front_color == "rb":
        color_dict, color_bar, min_y, max_y, dy = rb(dataset["data"], dataset["double"])

    else:
        print("???")
        sys.exit()

    for i in dataset["front"].keys():    
        poly = plt.Polygon(dataset["front"][i], fc=color_dict[i])
        ax.add_patch(poly)
    x_back = [x for i in dataset["back"].keys() for x,_ in dataset["back"][i]]
    y_back = [y for i in dataset["back"].keys() for _,y in dataset["back"][i]]
    xmin = min(x_back)
    xmax = max(x_back)
    ymin = min(y_back)
    ymax = max(y_back)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    if title:
        ax.set_title(title)

    for i,c in zip(np.linspace(min_y, max_y, 256), color_bar):
        poly = plt.Polygon(((0,i),(1,i),(1,i+dy),(0,i+dy)), fc=c)
        ax_c.add_patch(poly)
    ax_c.set_xlim([0,1])
    ax_c.tick_params(labelbottom=False)
    ax_c.set_ylim([min_y, max_y])
    
    if save_name:
        plt.savefig(save_name)
    if show:
        plt.show()
    return