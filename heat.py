from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import shapefile, pickle
import numpy as np
from GySon.colormap import fill_color
from numpy.random import randn
from GySon.dataset import load_toyama_second, read_csv_data
from GySon.plot import heatmap

sf = load_toyama_second()
sf_data = read_csv_data(sf, "randomdata.csv")
heatmap(sf_data, title="test")