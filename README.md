# JupyThree

A Jupyter widget based on pythreejs to display massive pointclouds (millions of points)
with **excellent interactive speed**. Also handles triangular meshes, with easy per-vertex color or scalar field.

<img src="media/jupythree_basic.png" title="" alt="Basic usage" width="473">

![Colormaps](media/jupythree_colormaps.png)

```python
import numpy as np
from jupythree.pointcloud import pointcloud

N = 2000000 #<-- two million points
x = np.random.random((N,3))/2 - 0.25 # cube

pointcloud(x, color=x[:,1]).show()
```

## Installation

Clone this repo and install requirements

```
git clone https://github.com/groscot/jupythree
cd jupythree
pip install -r requirements.txt
```

> Installation through pip (`pip install ...`) will come soon 🙏

## Usage

Run the included Notebook `Jupythree Demo.ipynb`

## Requirements

- pythreejs
- numpy
- ipywidgets
- matplotlib (for colormaps)

## Some nice features:

1. Handles millions of points while keeping interactive rotation and zoom
2. RGB colors + real values with matplotlib colormaps
3. Slider controlling the radius: `pointcloud(x).with_slider().show()`
4. Realtime animations: create and display the pointcloud with one cell (`handle = pointcloud(x1); handle.show()`), animate it from any other cell of your notebook (`handle.update(pc=x2)`)
5. Triangular meshes with vertex colors: `mesh(V, F, vertex_color=V[:,0]).show()`

## Known issues:

In recent versions of Jupyter, you will have a warning when displaying the first pointcloud of a session. It affects other libraries based on WebGL (such as plotly). You can safely ignore this message.

```
UserWarning: Message serialization failed with:
Out of range float values are not JSON compliant
Supporting this message is deprecated in jupyter-client 7, please make sure your message is JSON-compliant
  content = self.pack(content)
```