import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = load_toyama_second_pos()
sf2 = shapefile.Reader("shp\\A32-13_16.shp", encoding="SHIFT-JIS")
sf3 = load_toyama_second()
for i, rec in enumerate(sf3["data"].keys()):
    if rec.split("立")[0] == "南砺市":
        for j, r in enumerate(sf2.records()):
            if r[2] in rec:
                sf3["front"][rec] = sf2.shape(j).points

f = open("toyama_second_shape_front.pkl", "wb")
pickle.dump(sf3["front"], f)
f.close()