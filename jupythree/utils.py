import numpy as np
from matplotlib import cm

scene_constants = {
    "camera_pos": [.8, .5, .8],
    "viewsize": 400,
}

color_tab10 = lambda i: cm.tab10(i)[:3]


def pointclouds(pc1, *args, show=False, **kwargs):
    """Quickly creates a composite pointcloud (automatic colors)"""
    from .pointcloud import pointcloud
    
    pointclouds = [pc1]
    if len(args) > 0: pointclouds += args
    
    # Recenter the whole pointcloud
    total_pc = np.vstack(pointclouds)
    mu = np.mean(total_pc, 0) # center
    M = np.max(total_pc-mu) # scale
    pc = (total_pc-mu)/M
    
    # set color
    colors = []
    for i,pc_ in enumerate(pointclouds):
        colors += [color_tab10(i)] * len(pc_)
        
    handle = pointcloud(pc, color=colors, **kwargs)
    if show:
        return handle.show()
    else:
        return handle
