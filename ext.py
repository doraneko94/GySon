import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt
import numpy as np

sf = load_toyama_second()
pos = set()
double = set()
for back in sf["back"].values():
    if back[0] == back[-1]:
        back = back[:-1]
    for b in back:
        if b in pos:
            double.add(b)
        else:
            pos.add(b)
lst = []
for back in sf["back"].values():
    if back[0] == back[-1]:
        back = back[:-1]
    temp = [1 for _ in back]
    for i in range(len(temp)):
        if back[i] in double:
            temp[i] = 0
    for i in range(len(temp)):
        if temp[i] == 0:
            if i+1<len(temp):
                pi = i+1
            else:
                pi = 0
            di = i-1
            if temp[pi] == 1 or temp[di] == 1:
                temp[i] = 2
    tmp = temp
    temp = []
    for i in range(len(tmp)):
        if tmp[i] > 0:
            temp.append(tmp[i])
    while len(temp) > 0:
        can = False
        for i in range(len(temp)):
            if temp[i-1] == 2 and temp[i] == 1:
                temp = temp[i-1:] + temp[:i-1]
                back = back[i-1:] + back[:i-1]
                for j in range(len(temp)-1):
                    if temp[j+1] == 2:
                        app = back[:j+2]
                        temp = temp[j+2:]
                        back = back[j+2:]
                        break
                lst.append(app)
                can = True
                break
        if can == False:
            break            
            
pos = lst[0]
lst = lst[1:]
while len(lst) > 0:
    can = False
    for l in lst:
        if pos[-1] == l[0]:
            pos += l
            lst.remove(l)
            can = True
            break
        if pos[-1] == l[-1]:
            pos += l[::-1]
            lst.remove(l)
            can = True
            break
        if pos[0] == l[-1]:
            pos = l + pos
            lst.remove(l)
            can = True
            break
        if pos[0] == l[0]:
            pos = l[::-1] + pos
            lst.remove(l)
            can = True
            break
    if can == False:
        break
print(lst)
fig, ax = plt.subplots()
poly = plt.Polygon(pos)
ax.add_patch(poly)
plt.xlim([137,138])
plt.ylim([36,37])
plt.show()