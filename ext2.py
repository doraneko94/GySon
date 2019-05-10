import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt
import numpy as np

sf = load_toyama_second()
keys = sf["back"].keys()
key = ["富山市2", "高岡市5", "魚津市", "氷見市12", "滑川市", "黒部市9", "砺波市", "小矢部市2", "南砺市", "射水市5", "射水市8", "舟橋村", "上市町2", "立山町", "入善町", "朝日町7"]

flag = 0
for i,pos in enumerate(sf["back"]["富山市2"]):
    if pos in sf["back"]["射水市5"] and flag == 0:
        start = pos
        starti = i
        flag = 1
    elif pos not in sf["back"]["射水市5"] and flag == 1:
        end = sf["back"]["富山市2"][i-1]
        endi = i
        break
p1 = sf["back"]["富山市2"][:starti+1]
p2 = sf["back"]["富山市2"][endi:]
for i, pos in enumerate(sf["back"]["射水市5"]):
    if pos == start:
        p3 = sf["back"]["射水市5"][:i+1]
    if pos == end:
        p4 = sf["back"]["射水市5"][i:]
if p1[0] == p2[0]:
    p1 = p2[::-1] + p1
elif p1[0] == p2[-1]:
    p1 = p2 + p1
elif p1[-1] == p2[0]:
    p1 += p2
elif p1[-1] == p2[-1]:
    p1 += p2[::-1]
if p3[0] == p4[0]:
    p3 = p4[::-1] + p3
elif p3[0] == p4[-1]:
    p3 = p4 + p3
elif p3[-1] == p4[0]:
    p3 += p4
elif p3[-1] == p4[-1]:
    p3 += p4[::-1]
if p1[-1] == p3[0]:
    p1 += p3
elif p1[-1] == p3[-1]:
    p1 += p3[::-1]

fig, ax = plt.subplots()
poly = plt.Polygon(p1, fc="b")
ax.add_patch(poly)
plt.xlim([136,138])
plt.ylim([36,37])
plt.show()