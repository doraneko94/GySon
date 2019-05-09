from matplotlib import pyplot as plt
import shapefile
import numpy as np

secf = open("town\\kurobe.txt", "r").read().split("\n")
names = [line for i, line in enumerate(secf) if i % 2 == 0]
towns = [line.split("、") for i, line in enumerate(secf) if i % 2 == 1]
    
sf = shapefile.Reader('town\h27ka16207.shp',encoding="SHIFT-JIS")
recs = sf.records()
rec_towns = [recs[i][6] for i in range(len(recs))]
#non = [[i for i in towns[j] if i not in rec_towns] for j in range(len(towns))]
#print(non)
"""
for i,x in enumerate(rec_towns):
    if "妙川寺" in x:
        print(x)
"""
town_lst = []
for i in range(len(towns)):
    town_lst += towns[i]
for i, x in enumerate(rec_towns):
    if x not in town_lst:
        print(x)
        print(rec_towns[i+1])
        town_g = i
        break
town_g = 0
sf_k = shapefile.Reader('shp\A32-13_16.shp',encoding="SHIFT-JIS")
recs_k = sf_k.records()
k_lst = [i for i in range(len(recs_k)) if recs_k[i][1] == "黒部市"]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
yes_all = [[rec_towns.index(x) for x in towns[i] if x in rec_towns]for i in range(4)]

for x,c in zip(yes_all, ["r", "b", "y", "k"]):
    for i in x:
        poly = plt.Polygon(tuple(sf.shape(i).points), fc=c)
        ax.add_patch(poly)
poly = plt.Polygon(tuple(sf.shape(town_g).points), fc="g")
ax.add_patch(poly)
yes = []
for i in yes_all:
    yes += i
yes += [town_g]
for i in k_lst:
    kx = [x for x,y in tuple(sf_k.shape(i).points)]
    ky = [y for x,y in tuple(sf_k.shape(i).points)]
    plt.plot(kx, ky)
yes_k = []
for i in k_lst:
    yes_k.append(i)
xmin = min([x for i in yes for x,y in sf.shape(i).points])
xmax = max([x for i in yes for x,y in sf.shape(i).points])
ymin = min([y for i in yes for x,y in sf.shape(i).points])
ymax = max([y for i in yes for x,y in sf.shape(i).points])
kxmin = min([x for i in yes_k for x,y in sf_k.shape(i).points])
kxmax = max([x for i in yes_k for x,y in sf_k.shape(i).points])
kymin = min([y for i in yes_k for x,y in sf_k.shape(i).points])
kymax = max([y for i in yes_k for x,y in sf_k.shape(i).points])
xmin = min([xmin, kxmin])
xmax = max([xmax, kxmax])
ymin = min([ymin, kymin])
ymax = max([ymax, kymax])
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
plt.show()