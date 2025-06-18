from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..resource.bind_group import BindGroupLayout, BindGroup

from . import GlobalBindGroupIndex


class ViewportBindIndex:
    VIEWPORT_UNIFORM = 0


@klass.singleton
class ViewportBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=ViewportBindIndex.VIEWPORT_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries=entries, label="Viewport Bind Group Layout")


class ViewportBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = GlobalBindGroupIndex.VIEWPORT,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=ViewportBindIndex.VIEWPORT_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(
            entries=entries, layout=ViewportBindGroupLayout(), label="Viewport Bind Group", index=index
        )
