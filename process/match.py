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

for j in [1]:
    print(names[j])
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    yes = [rec_towns.index(x) for x in towns[j] if x in rec_towns]
    for i in yes:
        poly = plt.Polygon(tuple(sf.shape(i).points), fc="r")
        ax.add_patch(poly)
    xmin = min([x for i in yes for x,y in sf.shape(i).points])
    xmax = max([x for i in yes for x,y in sf.shape(i).points])
    ymin = min([y for i in yes for x,y in sf.shape(i).points])
    ymax = max([y for i in yes for x,y in sf.shape(i).points])
    plt.xlim([xmin,xmax])
    plt.ylim([ymin,ymax])
    plt.show()