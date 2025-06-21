from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..resource.bind_group import BindGroupLayout, BindGroup

from . import BindGroupIndex


class ViewportBindIndex:
    VIEWPORT_UNIFORM = 0
    TEXTURE = 1
    SAMPLER = 2


@klass.singleton
class ViewportBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=ViewportBindIndex.VIEWPORT_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=ViewportBindIndex.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=ViewportBindIndex.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
        ]
        super().__init__(entries=entries, label="Viewport Bind Group Layout")


class ViewportBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        texture_view: wgpu.TextureView,
        sampler: wgpu.Sampler,
        index: int = BindGroupIndex.VIEWPORT,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=ViewportBindIndex.VIEWPORT_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=ViewportBindIndex.TEXTURE, texture_view=texture_view
            ),
            wgpu.BindGroupEntry(binding=ViewportBindIndex.SAMPLER, sampler=sampler),
        ]

        super().__init__(
            entries=entries, layout=ViewportBindGroupLayout(), label="Viewport Bind Group", index=index
        )
