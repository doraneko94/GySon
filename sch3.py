import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = load_toyama_second_pos()
sf2 = load_toyama_second()

for i, sch1 in enumerate(sf.keys()):
    fig, ax = plt.subplots()
    for j, sch2 in enumerate(sf2["data"]):
        if sch1 in sch2:
            poly = plt.Polygon(sf2["front"][sch2])
            ax.add_patch(poly)
            print(sch2)
    ax.plot(sf[sch1][0][0], sf[sch1][0][1], "o", c="r")
    plt.show()