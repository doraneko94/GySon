from matplotlib import pyplot as plt
import shapefile
import numpy as np

secf = open("town\\kurobe.txt", "r").read().split("\n")
names = [line for i, line in enumerate(secf) if i % 2 == 0]
towns = [line.split("、") for i, line in enumerate(secf) if i % 2 == 1]
    
sf = shapefile.Reader('town\h27ka16207.shp',encoding="SHIFT-JIS")
recs = sf.records()
rec_towns = [recs[i][6] for i in range(len(recs))]
non = [[i for i in towns[j] if i not in rec_towns] for j in range(len(towns))]
print(non)
"""
for i,x in enumerate(rec_towns):
    if "妙川寺" in x:
        print(x)
"""
town_lst = []
for i in range(len(towns)):
    town_lst += towns[i]
for i in rec_towns:
    if i not in town_lst:
        print(i)
"""
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

yes = [i for i,x in enumerate(towns[0]) if x in rec_towns]
for i in yes:
    poly = plt.Polygon(tuple(sf.shape(i).points), fc="r")
    ax.add_patch(poly)

plt.xlim([137.18,137.23])
plt.ylim([36.68,36.72])
plt.show()

"""