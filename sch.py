import shapefile
from GySon.dataset import load_toyama_second, read_csv_data, load_toyama_second_pos
import pickle
from matplotlib import pyplot as plt

sf = shapefile.Reader("sch\\P29-13_16.shp", encoding="SHIFT-JIS")
data = {}
for i, rec in enumerate(sf.records()):
    if rec[2] == "16002" or (rec[2] == "99999" and rec[4] == "新湊中学校"):
        if rec[4] in ["富山大学人間発達科学部附属中学校", "片山学園中学校", "新湊西部中学校", "奈古中学校"]:
            continue
        if rec[0] == "16201":
            rec[4] = "富山市立" + rec[4]
        if rec[0] == "16202":
            rec[4] = "高岡市立" + rec[4]
        if rec[0] == "16204":
            rec[4] = "魚津市立" + rec[4]
        if rec[0] == "16205":
            rec[4] = "氷見市立" + rec[4]
        if rec[0] == "16206":
            rec[4] = "滑川市立" + rec[4]
        if rec[0] == "16207":
            rec[4] = "黒部市立" + rec[4]
        if rec[0] == "16208":
            rec[4] = "砺波市立" + rec[4]
        if rec[0] == "16209":
            rec[4] = "小矢部市立" + rec[4]
        if rec[0] == "16210":
            rec[4] = "南砺市立" + rec[4]
        if rec[0] == "16211":
            rec[4] = "射水市立" + rec[4]
        if rec[0] == "16321":
            rec[4] = "舟橋村立" + rec[4]
        if rec[0] == "16322":
            rec[4] = "上市町立" + rec[4]
        if rec[0] == "16323":
            rec[4] = "立山町立" + rec[4]
        if rec[0] == "16342":
            rec[4] = "入善町立" + rec[4]
        if rec[0] == "16343":
            rec[4] = "朝日町立" + rec[4]
        data[rec[4]] = sf.shape(i).points[0]
f = open("toyama_second_pos.pkl", "wb")
pickle.dump(data, f)
f.close()