import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt
from GySon.interpolation import semivariogram, kriging_mtx
import numpy as np
from GySon.plot import heatmap
from matplotlib.colors import LinearSegmentedColormap

cdict = {"red":     ((0.0, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 1.0, 1.0)),
         "green":   ((0.0, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 0.0, 0.0)),
         "blue":    ((0.0, 1.0, 1.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
        }

mycm = LinearSegmentedColormap("mycm", cdict)

np.random.seed(42)
sf = load_toyama_second_pos()
sf2 = load_toyama_second()
xyv_dict = {}
for key in sf.keys():
    xyv_dict[key] = [sf[key], (sf[key][0]-36) + (sf[key][1]-136) + np.random.random()*2 - 1.0]
    for k in sf2["data"].keys():
        if key in k:
            sf2["data"][k] = xyv_dict[key][1]
heatmap(sf2, title="heat", save_name="heat.png")
xy = np.array([xyv_dict[key][0] for key in sf.keys()])
v = np.array([xyv_dict[key][1] for key in sf.keys()])

param, lag_h, fitting_range, selected_model = semivariogram(xy, v, lag_h=0.02, fitting_range=0.3, plot=True, plot_raw=True)
print(lag_h, fitting_range, selected_model)

x_back = [x for i in sf2["back"].keys() for x,_ in sf2["back"][i]]
y_back = [y for i in sf2["back"].keys() for _,y in sf2["back"][i]]
xmin = min(x_back)
xmax = max(x_back)
ymin = min(y_back)
ymax = max(y_back)

xy_lim = [[xmin, xmax], [ymin, ymax]]
size = [9, 8]

krig_mtx, x_arr, y_arr = kriging_mtx(xy_lim, size, xy, v, param, selected_model)
xy_arr = np.array([[x, y] for x in x_arr for y in y_arr])

fig, ax = plt.subplots(figsize=(9, 8))
poly = plt.Polygon(sf2["ext"], fc="w")
ax.add_patch(poly)
plt.xlim(xy_lim[0])
plt.ylim(xy_lim[1])
plt.title("kriging")
sc = plt.scatter(xy_arr.T[0], xy_arr.T[1], c=krig_mtx.flatten(), s=1, cmap=mycm)
fig.colorbar(sc, ax=ax)
plt.savefig("kriging.png")
plt.show()
