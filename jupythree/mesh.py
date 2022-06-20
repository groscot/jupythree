import numpy as np
from pythreejs import (BufferAttribute, BufferGeometry, Mesh,
                       MeshLambertMaterial, MeshStandardMaterial)

from .colorable import colorable


class mesh(colorable):
    """
    A 3D tri-mesh which can live in the same window as a pointcloud
    """
    default_color = u"#ffffff"
    vertex_color = None
    wireframe_material = None
    V = None
    F = None
    
    def __init__(self,
        V,
        F,
        constant_color=None,
        faceopacity=1.,
        vertex_color=None,
        linecolor=u"#aaaaaa",
        lineopacity=0.,
        *args, **kwargs
    ):
        """
        Parameters:
        - V: a Nx3 array of floats
        - F: a Mx3 array of ints (3 indices of V per triangle face)
        - constant_color: [r,b,g] list/tuple/array in [0,1], colors the whole mesh
        - faceopacity: only works with a constant_color
        - vertex_color: for each vertex, either a scalar or an [r,g,b] color (bypasses constant_color)
        - linecolor/opacity: to include a wireframe of the mesh
        - normalize_colors (inherited from colorable): remap colors to the full [0,1] range
        """
        super(mesh, self).__init__(*args, **kwargs)
        
        self.l = len(V.reshape(-1,3))
        self._prepare_material(
            constant_color=constant_color,
            faceopacity=faceopacity,
            vertex_color=vertex_color,
            linecolor=linecolor,
            lineopacity=lineopacity
        )
        self._prepare_geometry(
            V, F
        )

        self.mesh = Mesh(
            geometry=self.geometry,
            material=self.mesh_material
        )
        self.children = [self.mesh]
        if self.wireframe_material is not None:
            self.wireframe = Mesh(
                geometry=self.geometry,
                material=self.wireframe_material
            )
            self.children.append(self.wireframe)

    def update(self,
        V=None, F=None,
        constant_color=None,
        faceopacity=1.,
        vertex_color=None,
        linecolor=u"#aaaaaa",
        lineopacity=0.,
    ):
        """
        You can select which parameter to update. For instance if updating V, F will remain the same, etc.
        """
        self._prepare_material(
            constant_color=constant_color,
            faceopacity=faceopacity,
            vertex_color=vertex_color,
            linecolor=linecolor,
            lineopacity=lineopacity
        )
        self._prepare_geometry(
            V, F
        )
        self.mesh.geometry = self.geometry
        if self.wireframe_material is not None:
            self.wireframe.geometry = self.geometry
                
        self.mesh.material = self.mesh_material
        if self.wireframe_material is not None:
            self.wireframe.material = self.wireframe_material

    def _prepare_material(self,
        constant_color=None,
        faceopacity=1.,
        vertex_color=None,
        linecolor=u"#aaaaaa",
        lineopacity=0.
    ):
        if vertex_color is not None:
            self.mesh_material = MeshLambertMaterial(
                vertexColors='VertexColors',
                side='DoubleSide'
            )
            self.vertex_color = self.input_color(vertex_color)
        else:
            constant_color = constant_color or self.default_color
            self.mesh_material = MeshStandardMaterial(
                color=constant_color,
                transparent=True,
                opacity=faceopacity,
                side='DoubleSide' #<-- makes the faces visible from both sides (disables backface culling)
            )
            self.vertex_color = None
        if lineopacity > 0:
            self.wireframe_material = MeshStandardMaterial(
                color=linecolor,
                transparent=True,
                opacity=lineopacity,
                side='DoubleSide',
                wireframe=True
            )
    
    def _prepare_geometry(self, V=None, F=None):
        self.V = V.astype(np.float32) if V is not None else self.V
        #* conversion to UINT32 type is important! it doesnt work without!
        self.F = F.astype(np.uint32).ravel() if F is not None else self.F
       
        self.l = len(self.V.reshape(-1,3))
        
        attributes = dict(
            position=BufferAttribute(self.V)
        )
        if self.vertex_color is not None:
            attributes["color"] = BufferAttribute(self.vertex_color)
        
        geometry = BufferGeometry(
            index = BufferAttribute(self.F),
            attributes=attributes
        )
        geometry.exec_three_obj_method('computeFaceNormals')
        geometry.exec_three_obj_method('computeVertexNormals')
        
        self.geometry = geometry
