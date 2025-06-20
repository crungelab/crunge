from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ...loader.shader_loader import ShaderLoader

from ..program_2d import Program2D
from ..render_pipeline_2d import RenderPipeline2D


@klass.singleton
class SpriteProgram(Program2D):
    def __init__(self):
        super().__init__()
        self.render_pipeline: RenderPipeline2D = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "sprite.wgsl"
        )

        self.render_pipeline = RenderPipeline2D(
            vertex_shader_module=shader_module, fragment_shader_module=shader_module
        ).create()
