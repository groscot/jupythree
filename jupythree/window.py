import ipywidgets as widgets
from pythreejs import *

from .utils import scene_constants


class window:
    """
    Jupyter widget to display a 3D scene. To display, call .show() method
    Other components will inherit this class, such as pointcloud and mesh
    """
    antialias = True
    children = []
    sliders = []
    renderer = None
    title = None
    controller = None
    camera = None
    
    def __init__(self,
            children,
            *additional,
            width=None, height=None,
            projection=None,
            controller=None,
            master=None,
            title=None
            ):
        """
        Parameters of the window: width, height, title
        Set master to another window object in order to synchronize views
        """
        input_children = children if type(children) == list else [children]
        if len(additional) > 0:
            input_children += additional
        self.children = []
        self.sliders = []
        for child in input_children:
            self.children += getattr(child, 'children', [])
            if hasattr(child, 'slider'):
                self.sliders.append(child.slider)
        width = width or scene_constants['viewsize']
        height = height or scene_constants['viewsize']
        self.width = width
        self.height = height
        self.title = title
        self._make_camera(projection=projection, controller=controller, master=master)
        self._make_lights()
    
    def show(self):
        if self.renderer is None:
            self._make_renderer()
        elements = []
        if len(self.sliders):
            elements.append(widgets.VBox(self.sliders))
        elements.append(self.renderer)
        if self.title is not None:
            elements.append(widgets.HTML(f"<center>{self.title}</center"))
        return widgets.Box([widgets.VBox(elements)])
    
    def _make_camera(self, projection=None, controller=None, master=None):
        if master is None:
            if projection == "orthographic":
                self.camera = OrthographicCamera(-1, 1, -1, 1, -1, 1)
            else:
                self.camera = PerspectiveCamera(position=scene_constants['camera_pos'],
                                                aspect=self.width/self.height)
            self.controller = controller or OrbitControls(controlling=self.camera)
        else:
            self.camera = master.camera
            self.controller = master.controller
            
    def _make_lights(self):
        self.key_light = DirectionalLight(position=[.5, 1, 0], intensity=.3)
        self.ambient_light = AmbientLight(intensity=.8)

    def _make_renderer(self):
        all_children = self.children + [self.camera, self.key_light, self.ambient_light]
        self.scene = Scene(children=all_children)
        self.renderer = Renderer(camera=self.camera, scene=self.scene, controls=[self.controller],
            width=self.width, height=self.height, antialias=self.antialias)
