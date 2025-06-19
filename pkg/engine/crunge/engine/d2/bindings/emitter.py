from loguru import logger

from crunge import wgpu
from crunge.core import klass

from .model import ModelBindGroupLayoutBase, ModelBindGroup
from . import BindGroupIndex


class EmitterBindIndex:
    MODEL_UNIFORM = 0
    PARTICLE_STORAGE = 1


@klass.singleton
class EmitterBindGroupLayout(ModelBindGroupLayoutBase):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=EmitterBindIndex.PARTICLE_STORAGE,
                visibility=wgpu.ShaderStage.COMPUTE | wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]

        super().__init__(entries=entries, label="Emitter Bind Group Layout")


class EmitterBindGroup(ModelBindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        storage_buffer: wgpu.Buffer,
        storage_buffer_size: int,
        index: int = BindGroupIndex.MODEL,
        layout=EmitterBindGroupLayout(),
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=EmitterBindIndex.PARTICLE_STORAGE,
                buffer=storage_buffer,
                size=storage_buffer_size,
            ),
        ]

        super().__init__(
            uniform_buffer,
            uniform_buffer_size,
            entries=entries,
            layout=layout,
            label="Emitter Bind Group",
            index=index,
        )
