from jinja2 import Environment

from crunge import gltf

from ...d3.scene_3d import Scene3D


class BuilderContext:
    def __init__(self, scene: Scene3D, tf_model: gltf.Model, template_env: Environment) -> None:
        self.scene = scene
        self.tf_model = tf_model
        self.template_env = template_env

        from .shader import VertexShaderBuilder, FragmentShaderBuilder
        #from .shader_ng import VertexShaderBuilder, FragmentShaderBuilder

        self.vertex_shader_builder_class = VertexShaderBuilder
        self.fragment_shader_builder_class = FragmentShaderBuilder
