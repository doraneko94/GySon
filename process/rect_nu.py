from matplotlib import pyplot as plt
import shapefile, pickle
import numpy as np

secf = open("town\\nyuzen.txt", "r").read().split("\n")
names = [line for i, line in enumerate(secf) if i % 2 == 0]
towns = [line.split("、") for i, line in enumerate(secf) if i % 2 == 1]
    
sf = shapefile.Reader('town\h27ka16342.shp',encoding="SHIFT-JIS")
recs = sf.records()
rec_towns = [recs[i][6] for i in range(len(recs))]
point_dict = {}
for tn in range(len(towns)):
    ps = [sf.shape(rec_towns.index(x)).points for x in towns[tn]]

    ps_all = []
    for i in ps:
        ps_all += i[:-1]
    ps_1 = [i for i in set(ps_all) if ps_all.count(i) > 1]
    ps_2 = []
    point = []
    for p in ps:
        tf = [1 for _ in range(len(p))]
        for i in range(len(p)):
            if p[i] in ps_1:
                tf[i] = 0
        tf = [tf[-1]] + tf + [tf[0]]
        for i in range(len(p)):
            if tf[i+1] == 0:
                if tf[i] == 1 or tf[i+2] == 1:
                    if p[i] not in ps_2:
                        ps_2.append(p[i])
    for p in ps:
        tf = [1 for _ in range(len(p))]
        for i in range(len(p)):
            if (p[i] in ps_1) and (p[i] not in ps_2):
                tf[i] = 0
        j = 0
        if tf[0] == 1 and tf[-1] == 1:
            lim = len(tf)
            p = p+p
            tf = tf+tf
            p_key = 1
            while j < len(tf):
                if tf[j] == 1:
                    if p_key != 1:
                        lst = []
                        k_max = len(tf)-j
                        for k in range(k_max):
                            if tf[j] == 0:
                                point.append(lst)
                                break
                            lst.append(p[j])
                            j += 1
                            if k == k_max-1:
                                point.append(lst)
                    else:
                        j += 1
                else:
                    if j < lim:
                        p_key = 0
                    else:
                        p_key = 1
                    j += 1
        else:
            while j < len(tf):
                if tf[j] == 1:
                    lst = []
                    k_max = len(tf)-j
                    for k in range(k_max):
                        if tf[j] == 0:
                            point.append(lst)
                            break
                        lst.append(p[j])
                        j += 1
                        if k == k_max-1:
                            point.append(lst)
                else:
                    j += 1
    p_lst = point[0]
    head = [p[0] for p in point[1:]]
    foot = [p[-1] for p in point[1:]]
    point.pop(0)
    #point_lst = [q for p in point[1:] for q in p]
    #print(p_lst[-1] in point_lst)

    for i in range(len(point)):
        if p_lst[-1] not in head:
            if p_lst[-1] not in foot:
                break
            else:
                one = p_lst[-1]
                p_lst += point[foot.index(one)][::-1][1:]
                point.pop(foot.index(one))
                head.pop(foot.index(one))
                foot.pop(foot.index(one))
                #print("a")
        else:
            one = p_lst[-1]        
            p_lst += point[head.index(one)][1:]
            point.pop(head.index(one))
            foot.pop(head.index(one))
            #print(head.index(one))
            head.pop(head.index(one))

    for i in range(len(point)):
        if p_lst[0] not in foot:
            if p_lst[0] not in head:
                #print("end")
                break
            else:
                one = p_lst[0]
                p_lst = point[head.index(one)][::-1][:-1] + p_lst
                point.pop(head.index(one))
                foot.pop(head.index(one))
                head.pop(head.index(one))
                #print("a")
        else:
            one = p_lst[0]        
            p_lst = point[foot.index(one)][:-1] + p_lst
            point.pop(foot.index(one))
            head.pop(foot.index(one))
            #print(foot.index(one))
            foot.pop(foot.index(one))
    #print(p_lst)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #poly = plt.Polygon(p_lst, fc="r")
    #ax.add_patch(poly)
    #poly = plt.Polygon(point[21], fc="g")
    #ax.add_patch(poly)

    yes = [rec_towns.index(x) for x in towns[tn] if x in rec_towns]
    for i in yes:
        poly = plt.Polygon(tuple(sf.shape(i).points), fc="r", ec="k")
        ax.add_patch(poly)
    xmin = min([x for i in yes for x,y in sf.shape(i).points])
    xmax = max([x for i in yes for x,y in sf.shape(i).points])
    ymin = min([y for i in yes for x,y in sf.shape(i).points])
    ymax = max([y for i in yes for x,y in sf.shape(i).points])
    plt.xlim([xmin,xmax])
    plt.ylim([ymin,ymax])

    px = [x for x,y in p_lst]
    py = [y for x,y in p_lst]
    plt.plot(px, py, color="g")

    plt.show()
    #print(p_lst[-1])
    point_dict[names[tn]] = p_lst
    #print(tn, names[tn])
    print(p_lst[-1])
with open("nyuzenmachi_kouku.pkl", "wb") as f:
    pickle.dump(point_dict, f)
f.close()