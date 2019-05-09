from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import shapefile, pickle
import numpy as np
from colormap import fill_color
from numpy.random import randn

with open("toyamashi_kouku.pkl", "rb") as f:
    toyamashi = pickle.load(f)
f.close()
with open("namerikawashi_kouku.pkl", "rb") as f:
    namerikawashi = pickle.load(f)
f.close()
with open("nyuzenmachi_kouku.pkl", "rb") as f:
    nyuzenmachi = pickle.load(f)
f.close()
sf = shapefile.Reader('shp\A32-13_16.shp',encoding="SHIFT-JIS")
recs = sf.records()
name_lst0 = [i[1]+"立"+i[2] if "新川郡" not in i[1] else i[1].split("新川郡")[1]+"立"+i[2] for i in recs]
name_lst0.remove("南砺市立白地")
toyama_lst = ["富山市立"+i+"中学校" for i in toyamashi.keys()]
namerikawa_lst = ["滑川市立"+i+"中学校" for i in namerikawashi.keys()]
nyuzen_lst = ["入善町立"+i+"中学校" if "西" in i else "入善町立入善中学校" for i in nyuzenmachi.keys()]
name_lst = name_lst0 + toyama_lst + namerikawa_lst + nyuzen_lst
name_set = set(name_lst)
double = [i for i in name_set if name_lst.count(i) > 1]
double_num = [0 for _ in double]
for i,n in enumerate(name_lst):
    if n in double:
        double_num[double.index(n)] += 1
        name_lst[i] += str(double_num[double.index(n)])
name_lst0 = name_lst[:len(name_lst0)]
toyama_lst = name_lst[len(name_lst0):len(name_lst0)+len(toyama_lst)]
namerikawa_lst = name_lst[len(name_lst0)+len(toyama_lst):len(name_lst0)+len(toyama_lst)+len(namerikawa_lst)]
nyuzen_lst = name_lst[len(name_lst0)+len(toyama_lst)+len(namerikawa_lst):]
shape_dict = {}
for i,x in enumerate(name_lst0):
    shape_dict[x] = tuple(sf.shape(i).points)
for x,k in zip(toyama_lst, toyamashi.keys()):
    shape_dict[x] = toyamashi[k]
for x,k in zip(namerikawa_lst, namerikawashi.keys()):
    shape_dict[x] = namerikawashi[k]
for x,k in zip(nyuzen_lst, nyuzenmachi.keys()):
    shape_dict[x] = nyuzenmachi[k]

with open("toyama_second_shape_front.pkl", "wb") as f:
    pickle.dump(shape_dict, f)
f.close()

with open("toyama_second_double.pkl", "wb") as f:
    pickle.dump(double, f)
f.close()

mu = 0
sigma = 1
data_dict = {}
for i,x in enumerate(name_set):
    if x in double:
        for j in range(double_num[double.index(x)]):
            data_dict[x+str(j+1)] = 0
    else:
        data_dict[x] = 0

with open("toyama_second_data.pkl", "wb") as f:
    pickle.dump(data_dict, f)
f.close()


fig = plt.figure(figsize=(9,8))
gs_master = GridSpec(nrows=1, ncols=2, width_ratios=[8, 1])
gs_1 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 0])
ax = fig.add_subplot(gs_1[:, :])
gs_2 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 1])
ax_c = fig.add_subplot(gs_2[:, :])
sf_toyama = shapefile.Reader("town\\N03-18_16_180101.shp", encoding="SHIFT-JIS")
recs_toyama = sf_toyama.records()
names_toyama = [i[3] for i in recs_toyama]
toyama_dict = {}
name_set_toyama = set(names_toyama)
double_toyama = [i for i in name_set_toyama if names_toyama.count(i) > 1]
double_num_toyama = [0 for _ in double_toyama]
for i,n in enumerate(names_toyama):
    if n in double_toyama:
        double_num_toyama[double_toyama.index(n)] += 1
        names_toyama[i] += str(double_num_toyama[double_toyama.index(n)])
for i in range(len(recs_toyama)):
    poly = plt.Polygon(tuple(sf_toyama.shape(i).points), fc="0.0")
    toyama_dict[names_toyama[i]] = tuple(sf_toyama.shape(i).points)
    ax.add_patch(poly)

with open("toyama_second_shape_back.pkl", "wb") as f:
    pickle.dump(toyama_dict, f)
f.close()

for i in shape_dict.keys():
    poly = plt.Polygon(shape_dict[i], fc=fill_color(data_dict[i], mu, sigma))
    ax.add_patch(poly)
xmin = min([x for i in range(len(recs_toyama)) for x,y in sf_toyama.shape(i).points])
xmax = max([x for i in range(len(recs_toyama)) for x,y in sf_toyama.shape(i).points])
ymin = min([y for i in range(len(recs_toyama)) for x,y in sf_toyama.shape(i).points])
ymax = max([y for i in range(len(recs_toyama)) for x,y in sf_toyama.shape(i).points])
ax.set_xlim([xmin,xmax])
ax.set_ylim([ymin,ymax])

max_x = 128/60*sigma
min_x = -max_x
dx = (max_x-min_x)/255
for i in np.linspace(min_x, max_x, 256):
    poly = plt.Polygon(((0,i),(1,i),(1,i+dx),(0,i+dx)), fc=fill_color(i, mu, sigma))
    ax_c.add_patch(poly)
ax_c.set_xlim([0,1])
ax_c.set_ylim([min_x, max_x])
plt.savefig("randn.png")
plt.show()