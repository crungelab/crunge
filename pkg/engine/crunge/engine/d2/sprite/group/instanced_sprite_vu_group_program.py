from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ....resource.bind_group.bind_group_layout import BindGroupLayout
from ....loader.shader_loader import ShaderLoader

from ...program_2d import Program2D
from ...render_pipeline_2d import RenderPipeline2D


@klass.singleton
class ModelBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]
        super().__init__(entries=entries, label="ModelBindGroupLayout")


class InstancedSpriteVuGroupRenderPipeline(RenderPipeline2D):
    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout()

@klass.singleton
class InstancedSpriteVuGroupProgram(Program2D):
    def __init__(self):
        super().__init__()
        self.render_pipeline: InstancedSpriteVuGroupRenderPipeline = None
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = ShaderLoader(self.template_env, self.template_dict).load(
            "instanced_sprite.wgsl"
        )

        self.render_pipeline = InstancedSpriteVuGroupRenderPipeline(
            vertex_shader_module=shader_module, fragment_shader_module=shader_module
        ).create()
