from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ...loader.shader_loader import ShaderLoader

from ..program_2d import Program2D
from ..renderer.render_pipeline_2d import RenderPipeline2D


ADDITIVE_BLEND_STATE = wgpu.BlendState(
    alpha=wgpu.BlendComponent(
        operation=wgpu.BlendOperation.ADD,
        src_factor=wgpu.BlendFactor.ONE,
        dst_factor=wgpu.BlendFactor.ONE,
    ),
    color=wgpu.BlendComponent(
        operation=wgpu.BlendOperation.ADD,
        src_factor=wgpu.BlendFactor.SRC_ALPHA,
        dst_factor=wgpu.BlendFactor.ONE,
    ),
)

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


@klass.singleton
class AdditiveSpriteProgram(Program2D):
    """Same sprite.wgsl, additive blend state — same shader, different
    pipeline, since blend mode is baked in at pipeline creation and can't
    be switched per-draw-call in WebGPU."""

    def __init__(self):
        super().__init__()
        self.render_pipeline: RenderPipeline2D = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load("sprite.wgsl")
        self.render_pipeline = RenderPipeline2D(
            vertex_shader_module=shader_module,
            fragment_shader_module=shader_module,
            blend_state=ADDITIVE_BLEND_STATE,
        ).create()