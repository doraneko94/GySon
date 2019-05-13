import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = shapefile.Reader("sch\\P29-13_16.shp", encoding="SHIFT-JIS")
for i in sf.records():
    if "新湊" in i[4]:
        print(i) 