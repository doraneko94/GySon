import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = load_toyama_second_pos()
sf2 = shapefile.Reader("shp\\A32-13_16.shp", encoding="SHIFT-JIS")
sf3 = load_toyama_second()
fig, ax = plt.subplots()
poly = plt.Polygon(sf3["front"]["南砺市立城端中学校"])
ax.add_patch(poly)
plt.show()
"""
for i, rec in enumerate(sf2.records()):
    if rec[1] == "南砺市":
        print(rec[2])
        fig, ax = plt.subplots()
        poly = plt.Polygon(sf2.shape(i).points)
        ax.add_patch(poly)
        for j, r in enumerate(sf.keys()):
            if rec[2] in r:
                ax.plot(sf[r][0], sf[r][1], "o", c="r")
                break
        plt.show()
"""
print(sf3["front"].keys())