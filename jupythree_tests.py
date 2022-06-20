#%%

import numpy as np

import pointcloud as pc
from mesh import mesh
from utils import *
from window import window

# make some random pc

x = np.random.random((5000,3))/2 - 0.25
c = x[:, 1]

y = np.random.random((5000,3))/2 - 0.25
y /= 2*np.linalg.norm(y, axis=1, keepdims=True)
c2 = y[:, 1]

#%%

window(pc.pointcloud(x).with_slider(), pc.pointcloud(y/2, c2).with_slider()).show()
# %%
pointclouds(x, y/2, radius=2)

# %%
wa = pc.pointcloud(x).to_window(title="A")
wb = pc.pointcloud(y/2, c2).to_window(master=wa, title="B")

widgets.HBox([wa.show(), wb.show()])
# %% Mesh stuff

# %% Load
import pickle

some_data = pickle.load(open("../some_data.pick", "rb"))

points = some_data["points"]
g = some_data["g"]
V = some_data["V"]
F = some_data["F"]


# %%

vv = V.reshape(-1,3)
# %%
mm = mesh(vv,F,vertex_color=vv[:,1], normalize_colors=True)
mm.show()





# %%
from matplotlib import cm

# %%
mesh(vv, F,
     vertex_color=vv[:,1], normalize_colors=True,
     cmap=cm.jet).show()

# %%
mesh(vv, F,
     vertex_color=vv[:,1], normalize_colors=False,
     cmap=cm.rainbow).show()
# %%
mesh(vv, F,
     vertex_color=list(range(729)), normalize_colors=False,
     cmap=cm.rainbow).show()
# %%
