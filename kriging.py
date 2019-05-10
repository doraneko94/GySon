import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = load_toyama_second()
sf_data = read_csv_data(sf, "randomdata.csv")
print(sf["data"])