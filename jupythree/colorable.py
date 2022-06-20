import matplotlib as mpl
import numpy as np
from matplotlib import cm

from .window import window


class windowable:
    """
    Easily create a window() view for this component
    """
    def to_window(self, *args, **kwargs):
        return window(self, *args, **kwargs)
        
    def show(self, *args, **kwargs):
        return window(self, *args, **kwargs).show()


class colorable(windowable):
    """
    Components which take several types of color inputs
    Parameters:
    - cmap: a matplotlib.cm colormap, for instance cm.viridis (default)
    - normalize_colors: maps all channels to [0,1] range
    See colorable.input_color() for color options
    """
    is_scalar_field = False
    
    def __init__(self, cmap=cm.viridis, normalize_colors=False):
        self.cmap = cmap
        self.normalize_colors = normalize_colors
    
    def input_color(self, color):
        """
        Parses different types of inputs to set the color
        - one [r,g,b]: same color for all points (r,g,b in [0,1])
        - list for all points:
            + scalar value --> mapped with self.cmap
            + [r,g,b] value
        """
        if type(color) == list or type(color) == tuple:
            if len(color) == 3:
                return [color] * self.l # make a constant list (over all points)
            else:
                color = np.array(color)
        if type(color) == np.ndarray:
            # input: array np
            if (color.shape[0] != self.l):
                raise ValueError("Color must have same length as component: got %d, expected %d" % (color.shape[0], self.l))
            if (color.ndim == 1):
                return self.process_scalar_field(color)
            elif (color.shape[1] == 3):
                if self.normalize_colors:
                    color = color.copy() # without a .copy(), next lines would affect the input array
                    color -= np.min(color,0)
                    color /= np.max(color,0)
                return color.astype(np.float32)
            else:
                raise ValueError("Unknown input color second dimension: %d (must be 1 or 3)" % (color.shape[1]))
        else:
            raise ValueError("Unknown color type: %s" % type(color))

    def process_scalar_field(self, color):
        """
        Processes a scalar field
        """
        self.is_scalar_field = True
        m = color.min()
        M = color.max()
        x = (color - m)/(M - m)
        self.m = m
        self.M = M
        rgb = self.cmap(x)[..., 0:3] #only keep rgb values, discard alpha
        return rgb.astype(np.float32)

    def colorbar(self, size=6, orientation='horizontal'):
        """
        Displays the colorbar when a scalar field has been defined
        """
        if not self.is_scalar_field:
            print('No scalar field defined, abort')
            return
        fig, ax = mpl.pyplot.subplots(figsize=(size, 1))
        fig.subplots_adjust(bottom=0.5)
        norm = mpl.colors.Normalize(vmin=self.m, vmax=self.M)
        handle = mpl.colorbar.ColorbarBase(ax, cmap=self.cmap, norm=norm, orientation=orientation)
        fig.show()
