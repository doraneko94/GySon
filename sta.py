import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt
from GySon.interpolation import semivariogram
import numpy as np

sf = shapefile.Reader("sta\\S12-17_NumberOfPassengers.shp", encoding="SHIFT-JIS")
sta_dict = {}
for i, rec in enumerate(sf.records()):
    if rec[2] in ["あいの風とやま鉄道線", "氷見線", "城端線"] or (rec[2] == "高山線" and rec[1] == "西日本旅客鉄道"):
        if rec[0] in sta_dict.keys():
            sta_dict[rec[0]][0] += rec[-1]
        else:
            sta_dict[rec[0]] = [rec[-1], sf.shape(i).points[0]]
xy = np.array([sta_dict[key][1] for key in sta_dict.keys()])
v = np.array([sta_dict[key][0] for key in sta_dict.keys()])
xy = xy[v>0]
v = v[v>0]
param, lag_h, fitting_range, selected_model = semivariogram(xy, v, plot=True)
