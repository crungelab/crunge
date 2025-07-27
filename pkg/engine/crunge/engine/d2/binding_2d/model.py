from typing import List, Optional

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...binding import BindGroupLayout, BindGroup

from . import BindGroupIndex


class ModelBindIndex:
    MODEL_UNIFORM = 0


class ModelBindGroupLayoutBase(BindGroupLayout):
    def __init__(self, entries: Optional[List[wgpu.BindGroupLayoutEntry]] = [], label="Model Bind Group Layout") -> None:
        entries = list(entries)  # Ensure entries is a mutable list
        entries.extend(
            [
                wgpu.BindGroupLayoutEntry(
                    binding=ModelBindIndex.MODEL_UNIFORM,
                    visibility=wgpu.ShaderStage.VERTEX,
                    buffer=wgpu.BufferBindingLayout(
                        type=wgpu.BufferBindingType.UNIFORM
                    ),
                ),
            ]
        )

        super().__init__(entries=entries, label=label)

@klass.singleton
class ModelBindGroupLayout(ModelBindGroupLayoutBase):
    pass

@klass.singleton
class DynamicModelBindGroupLayout(BindGroupLayout):
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


class ModelBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        entries: List[wgpu.BindGroupEntry] = [],
        index: int = BindGroupIndex.MODEL,
        layout=ModelBindGroupLayout(),
        label="Model Bind Group"
    ) -> None:
        entries = list(entries)  # Ensure entries is a mutable list
        entries.extend([
            wgpu.BindGroupEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ])

        super().__init__(
            entries=entries, layout=layout, label=label, index=index
        )
