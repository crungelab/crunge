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
    """One node, in a uniform buffer. For a vu that draws itself."""

    def __init__(self, label="Node Bind Group Layout") -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=NodeBindIndex.NODE_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries=entries, label=label)


@klass.singleton
class DynamicNodeBindGroupLayout(BindGroupLayout):
    """A group of nodes, in a read-only storage buffer, indexed per
    instance. For a vu whose group draws it."""

    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=NodeBindIndex.NODE_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]
        super().__init__(entries=entries, label="Dynamic Node Bind Group Layout")


class NodeBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.NODE,
        layout=None,
        label="Node Bind Group",
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=NodeBindIndex.NODE_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]
        # Resolved here rather than as a default argument. A singleton
        # evaluated in the signature is built at import time, before the
        # device exists in some start orders — and it reads as though every
        # caller shares one layout by choice rather than by accident.
        if layout is None:
            layout = NodeBindGroupLayout()
        super().__init__(entries=entries, layout=layout, label=label, index=index)