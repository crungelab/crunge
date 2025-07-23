from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ....binding import BindGroupLayout, BindGroup

from .. import BindGroupIndex


class SpriteBindIndex:
    MATERIAL_UNIFORM = 0
    TEXTURE = 1
    SAMPLER = 2


@klass.singleton
class SpriteBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=SpriteBindIndex.MATERIAL_UNIFORM,
                # visibility=wgpu.ShaderStage.FRAGMENT,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=SpriteBindIndex.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=SpriteBindIndex.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
        ]

        super().__init__(entries=entries, label="Sprite Bind Group Layout")


class SpriteBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        texture_view: wgpu.TextureView,
        sampler: wgpu.Sampler,
        index: int = BindGroupIndex.MATERIAL,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=SpriteBindIndex.MATERIAL_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=SpriteBindIndex.TEXTURE, texture_view=texture_view
            ),
            wgpu.BindGroupEntry(binding=SpriteBindIndex.SAMPLER, sampler=sampler),
        ]

        super().__init__(
            entries=entries,
            layout=SpriteBindGroupLayout(),
            label="Sprite Bind Group",
            index=index,
        )
