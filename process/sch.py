from matplotlib import pyplot as plt
import shapefile
import numpy as np

sf = shapefile.Reader('sch\P29-13_16.shp',encoding="SHIFT-JIS")
recs = sf.records()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

lst = [i for i in range(len(recs)) if ("中学" in recs[i][4]) and (recs[i][0] == "16201") and (recs[i][4] != "富山大学人間発達科学部附属中学校") and (recs[i][4] != "片山学園中学校")]
for i in lst:
    print(recs[i][4])