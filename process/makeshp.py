import shapefile, pickle
import numpy as np

def read_shp(filename, encoding="SHIFT-JIS"):
    sf = shapefile.Reader(filename,encoding="SHIFT-JIS")
    return sf, sf.records()