from jinja2 import Environment

from crunge import gltf

from crunge.engine.d3.scene_3d import Scene3D

from crunge.engine.d3.mesh_3d import Mesh3D
from crunge.engine.resource.material import Material

class BuilderContext:
    def __init__(self, scene: Scene3D, tf_model: gltf.Model, template_env: Environment) -> None:
        self.scene = scene
        self.tf_model = tf_model
        self.template_env = template_env

        self.array_cache = {}
        self.mesh_cache: dict[int, Mesh3D] = {}
        self.material_cache: dict[int, Material] = {}

        from .shader import VertexShaderBuilder, FragmentShaderBuilder

        self.vertex_shader_builder_class = VertexShaderBuilder
        self.fragment_shader_builder_class = FragmentShaderBuilder

