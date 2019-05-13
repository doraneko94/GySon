import numpy as np
from matplotlib import pyplot as plt
from GySon.dataset import load_toyama_second
from matplotlib.colors import LinearSegmentedColormap

cdict = {"red":     ((0.0, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 1.0, 1.0)),
         "green":   ((0.0, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 0.0, 0.0)),
         "blue":    ((0.0, 1.0, 1.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
        }

mycm = LinearSegmentedColormap("mycm", cdict)
sf = load_toyama_second()
x = np.arange(100)
y = np.arange(100,200)
v = np.random.rand(100)
fig, ax = plt.subplots(figsize=(9, 8))
poly = plt.Polygon(sf["ext"], fc="k")
ax.add_patch(poly)
plt.scatter(x, y, c=v, s=0.8, cmap=mycm)
plt.show()