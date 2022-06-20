import ipywidgets as widgets
import numpy as np
from pythreejs import BufferAttribute, BufferGeometry, Points, ShaderMaterial

from .colorable import colorable

"(i) The default color is defined here in the vertex shader"
vertexShader = """
uniform float pointSize;
uniform float spherical;
uniform vec3 constColor;
varying vec3 pointColor;
varying float pointRadius;

void main() {
    vec4 pos = projectionMatrix * modelViewMatrix * vec4(position, 1.0);

#ifdef CONSTANT_DISPLAY_SIZE
    float rad = pointSize;
#else
    float rad = 10.0 * pointSize / pos.w;
#endif

    gl_PointSize = rad;
    gl_Position = pos;
  
    pointRadius = rad;
#ifdef USE_COLOR
    pointColor = color;
#else
    pointColor = vec3(1.0, 0.0, 0.0); // <-- set the default color HERE <--
#endif
}    
"""

"(i) The fragment shader mimicks a spherical appearance"
fragmentShader = """
uniform float spherical;
varying vec3 pointColor;
varying float pointRadius;

void main() {
    // Reject points outside the circle
    vec2 temp = gl_PointCoord - 0.5;

    float rad = 0.25;
    float f = dot(temp, temp);
    if (f > rad) discard;

    // antialiasing
    float delta = 1.25 / pointRadius;
    float antialias = smoothstep(rad, rad - delta, f);

    // Give a spherical feeling (inner shadow) to the circle
    gl_FragColor = vec4(pointColor - spherical*f, antialias);
}  
"""


class pointcloud(colorable):
    """
    A 3D pointcloud or scatterplot (does not show the axes). View configured to handle
    coordinates in [-0.5, 0.5].
    Parameters:
    - color: see colorable.input_color() for usage
    - radius: display radius. Value 1 is good for e.g. a 2048x3 pointcloud
    - is_constant_display_size: the spheres' radii is fixed in screen space
    - spherical: intensity of the gradient which mimicks the appearance of a sphere (0 = flat disc)
    """
    def __init__(self, pc, color=None, radius=1., is_constant_display_size=False, spherical=2.,
                 *args, **kwargs):
        super(pointcloud, self).__init__(*args, **kwargs)
        
        self._prepare_material(radius, is_constant_display_size, spherical, color is not None)
        self._prepare_geometry(pc, color)

        self.scatter = Points(
            geometry=self.geometry,
            material=self.material
        )
        self.children = [self.scatter]

    def update(self, pc=None, color=None, radius=None):
        """
        Updates properties of the displayed pointcloud. Note that if updating pc, color
        will be reset too (if kept to None, the default will be used)
        """
        if pc is not None or color is not None:
            self._prepare_geometry(pc, color)
            defines = dict(**self.material.defines)
            if color is not None:
                defines['USE_COLOR'] = 1
            else:
                defines.pop('USE_COLOR', None)
            self.material.defines = defines
        elif radius is not None:
            uniforms = dict(**self.material.uniforms)
            uniforms.update(pointSize=dict(value=radius))
            self.material.uniforms = uniforms
        self.material.needsUpdate = True
    
    def with_slider(self, min=None, max=None, step=None):
        """
        Returns a pointcloud object whose .show() function will include a slider controlling the radius
        """
        min = min or self.radius/4.
        max = max or self.radius*2.
        step = step or self.radius/16.
        self.slider = widgets.FloatSlider(value=self.radius, min=min, max=max, step=step, readout_format='.3f')
        self.slider.observe(self.update_uniforms)
        return self

    def update_uniforms(self, change):
        "Update the shader uniforms controlling sphere size"
        uniforms = dict(**self.material.uniforms)
        uniforms.update(pointSize=dict(value=self.slider.value))
        self.material.uniforms = uniforms
        self.material.needsUpdate = True

    def _prepare_material(self, radius=1., is_constant_display_size=False, spherical=2., is_use_color=False):
        """
        This should be called only once, in the constructor. To update the material, change values of
        self.material and then, self.material.needsUpdate = True
        """
        defines = dict()
        if is_constant_display_size: defines['CONSTANT_DISPLAY_SIZE'] = 1
        if is_use_color: defines['USE_COLOR'] = 1
        self.material = ShaderMaterial(
            uniforms = dict(
                pointSize=dict(value=radius),
                spherical=dict(value=spherical)
            ),
            defines = defines,
            vertexShader = vertexShader,
            fragmentShader = fragmentShader,
            transparent=True
        )
        self.radius = radius
    
    def _prepare_geometry(self, pc=None, color=None):
        if pc is not None:
            # only update the inner points if requested
            self.pclist = pc.astype(np.float32)
            self.l = pc.shape[0]
        if color is not None:
            colors = self.input_color(color)
            geometry = BufferGeometry(
                attributes=dict(
                    position=BufferAttribute(self.pclist),
                    color=BufferAttribute(colors)
                )
            )
        else:
            geometry = BufferGeometry(
                attributes=dict(
                    position=BufferAttribute(self.pclist)
                )
            )
        self.geometry = geometry
        if hasattr(self, 'scatter'):
            self.scatter.geometry = self.geometry
