import numpy as np

def fill_color(x, mu, sigma):
    return [max(255+min(0, (x-mu)/sigma * 120), 0)/255, max(0, 255-abs((x-mu)/sigma)*120)/255, max(255+min(0, -(x-mu)/sigma * 120), 0)/255]

def rb_lst(x, mu, sigma):
    return [max(255+min(0, (x-mu)/sigma * 120), 0)/255, max(0, 255-abs((x-mu)/sigma)*120)/255, max(255+min(0, -(x-mu)/sigma * 120), 0)/255]

def rb(data: dict, double=None):
    if double:
        double_key = [0 for _ in double]
        data_lst = []
        for i in data.keys():
            for j in double:
                if j in i:
                    if double_key[double.index(j)] == 0:
                        data_lst.append(data[i])
                        double_key[double.index(j)] = 1
                else:
                    data_lst.append(data[i])
    else:
        data_lst = np.array([data[i] for i in data.keys()])
    mu = np.mean(data_lst)
    sigma = np.std(data_lst)
    max_y = 128/60*sigma + mu
    min_y = -max_y + mu
    dy = (max_y-min_y)/255
    return {i:rb_lst(data[i], mu, sigma) for i in data.keys()}, [rb_lst(i, mu, sigma) for i in np.linspace(min_y, max_y, 256)], min_y, max_y, dy
