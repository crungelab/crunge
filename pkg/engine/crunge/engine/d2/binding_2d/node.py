from typing import List, Optional

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...binding import BindGroupLayout, BindGroup

from . import BindGroupIndex


class NodeBindIndex:
    NODE_UNIFORM = 0


@klass.singleton
class NodeBindGroupLayout(BindGroupLayout):
    def __init__(
        self,
        label="Node Bind Group Layout",
    ) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=NodeBindIndex.NODE_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        super().__init__(entries=entries, label=label)


class NodeBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.NODE,
        layout=NodeBindGroupLayout(),
        label="Node Bind Group",
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=NodeBindIndex.NODE_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(entries=entries, layout=layout, label=label, index=index)
