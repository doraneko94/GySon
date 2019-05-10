from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from GySon.dataset import load_toyama_second_pos
from GySon.colormap import rb
import numpy as np

def heatmap(dataset, save_name=None, front_color="rb", back_color="k", title=None, show=True, school=False):
    fig = plt.figure(figsize=(9,8))
    gs_master = GridSpec(nrows=1, ncols=2, width_ratios=[8, 1])
    gs_1 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 0])
    ax = fig.add_subplot(gs_1[:, :])
    gs_2 = GridSpecFromSubplotSpec(nrows=1, ncols=1, subplot_spec=gs_master[0, 1])
    ax_c = fig.add_subplot(gs_2[:, :])

    for i in dataset["back"].keys():
        poly = plt.Polygon(dataset["back"][i], fc=back_color)
        ax.add_patch(poly)

    if front_color == "rb":
        color_dict, color_bar, min_y, max_y, dy = rb(dataset["data"], dataset["double"])

    else:
        print("???")
        sys.exit()

    for i in dataset["front"].keys():    
        poly = plt.Polygon(dataset["front"][i], fc=color_dict[i])
        ax.add_patch(poly)
    x_back = [x for i in dataset["back"].keys() for x,_ in dataset["back"][i]]
    y_back = [y for i in dataset["back"].keys() for _,y in dataset["back"][i]]
    xmin = min(x_back)
    xmax = max(x_back)
    ymin = min(y_back)
    ymax = max(y_back)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    if title:
        ax.set_title(title)

    for i,c in zip(np.linspace(min_y, max_y, 256), color_bar):
        poly = plt.Polygon(((0,i),(1,i),(1,i+dy),(0,i+dy)), fc=c)
        ax_c.add_patch(poly)
    ax_c.set_xlim([0,1])
    ax_c.tick_params(labelbottom=False)
    ax_c.set_ylim([min_y, max_y])
    
    if school:
        sf2 = load_toyama_second_pos().values()
        x = []
        y = []
        for i in sf2:
            x.append(i[0])
            y.append(i[1])
        ax.plot(x, y, marker="o", linestyle="None")
    
    if save_name:
        plt.savefig(save_name)
    if show:
        plt.show()