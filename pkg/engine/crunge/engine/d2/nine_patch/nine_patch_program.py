from crunge.core import klass

from ...loader.shader_loader import ShaderLoader

from ..program_2d import Program2D
from ..renderer.render_pipeline_2d import RenderPipeline2D

from ..sprite.sprite_program import ADDITIVE_BLEND_STATE


@klass.singleton
class NinePatchProgram(Program2D):
    """Same bind group layouts and topology as SpriteProgram — the nine patch
    only reads `model` in the vertex stage, as the sprite does."""

    def __init__(self):
        super().__init__()
        self.render_pipeline: RenderPipeline2D = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "nine_patch.wgsl"
        )

        self.render_pipeline = RenderPipeline2D(
            vertex_shader_module=shader_module, fragment_shader_module=shader_module
        ).create()


@klass.singleton
class AdditiveNinePatchProgram(Program2D):
    def __init__(self):
        super().__init__()
        self.render_pipeline: RenderPipeline2D = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "nine_patch.wgsl"
        )
        self.render_pipeline = RenderPipeline2D(
            vertex_shader_module=shader_module,
            fragment_shader_module=shader_module,
            blend_state=ADDITIVE_BLEND_STATE,
        ).create()
