import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = shapefile.Reader("pref-japan.shp")

fig, ax = plt.subplots()
poly = plt.Polygon(sf.shape(4).points, fc="b")
ax.add_patch(poly)
plt.xlim([136,138])
plt.ylim([36,37])
plt.show()