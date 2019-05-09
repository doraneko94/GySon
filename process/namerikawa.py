from matplotlib import pyplot as plt
import shapefile
import numpy as np

secf = open("town\\namerikawa.txt", "r").read().split("\n")
names = [line for i, line in enumerate(secf) if i % 2 == 0]
towns = [line.split("、") for i, line in enumerate(secf) if i % 2 == 1]
    
sf = shapefile.Reader('town\h27ka16206.shp',encoding="SHIFT-JIS")
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


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
yes_y = [rec_towns.index(x) for x in towns[0] if x in rec_towns]
yes_s = [rec_towns.index(x) for x in towns[1] if x in rec_towns]
for i in yes_y:
    poly = plt.Polygon(tuple(sf.shape(i).points), fc="r")
    ax.add_patch(poly)
for i in yes_s:
    poly = plt.Polygon(tuple(sf.shape(i).points), fc="b")
    ax.add_patch(poly)
#poly = plt.Polygon(tuple(sf.shape(town_g).points), fc="g")
#ax.add_patch(poly)
yes = yes_y + yes_s
xmin = min([x for i in yes for x,y in sf.shape(i).points])
xmax = max([x for i in yes for x,y in sf.shape(i).points])
ymin = min([y for i in yes for x,y in sf.shape(i).points])
ymax = max([y for i in yes for x,y in sf.shape(i).points])
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
plt.show()