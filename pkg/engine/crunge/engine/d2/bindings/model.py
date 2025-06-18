from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...resource.bind_group import BindGroupLayout, BindGroup

from . import BindGroupIndex

class ModelBindIndex:
    MODEL_UNIFORM = 0

@klass.singleton
class ModelBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        super().__init__(entries=entries, label="Model Bind Group Layout")


class ModelBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.MODEL,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(
            entries=entries, layout=ModelBindGroupLayout(), label="Model Bind Group", index=index
        )
