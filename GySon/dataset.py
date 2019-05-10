import pickle
import pandas as pd

def load_toyama_second():
    data = {}
    with open("GySon\\data\\toyama_second_shape_front.pkl", "rb") as f:
        data["front"] = pickle.load(f)
    f.close()

    with open("GySon\\data\\toyama_second_shape_back.pkl", "rb") as f:
        data["back"] = pickle.load(f)
    f.close()

    with open("GySon\\data\\toyama_second_data.pkl", "rb") as f:
        data["data"] = pickle.load(f)
    f.close()

    with open("GySon\\data\\toyama_second_double.pkl", "rb") as f:
        data["double"] = pickle.load(f)
    f.close()
    return data

def load_toyama_second_pos():
    with open("GySon\\data\\toyama_second_pos.pkl", "rb") as f:
        data = pickle.load(f)
    f.close()
    return data

def read_csv_data(dataset, filename, encoding="SHIFT-JIS"):
    df = pd.read_csv(filename, encoding=encoding)
    for i,x in enumerate(df["name"]):
        for j in dataset["data"].keys():
            if x in j:
                dataset["data"][j] = float(df["data"][i])
    return dataset