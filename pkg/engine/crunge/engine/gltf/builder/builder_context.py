from crunge import gltf

from ...d3.scene_3d import Scene3D


class BuilderContext:
    def __init__(self, scene: Scene3D, tf_model: gltf.Model) -> None:
        super().__init__()
        self.scene = scene
        self.tf_model = tf_model

        #from .shader import VertexShaderBuilder, FragmentShaderBuilder
        from .shader_ng import VertexShaderBuilder, FragmentShaderBuilder

        self.vertex_shader_builder_class = VertexShaderBuilder
        self.fragment_shader_builder_class = FragmentShaderBuilder
