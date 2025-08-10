from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ....binding import BindGroupLayout, BindGroup

from .. import BindGroupIndex


class MaterialBindIndex:
    TEXTURE = 0
    SAMPLER = 1


@klass.singleton
class MaterialBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=MaterialBindIndex.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    #view_dimension=wgpu.TextureViewDimension.E2D,
                    view_dimension=wgpu.TextureViewDimension.E2D_ARRAY,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=MaterialBindIndex.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
        ]

        super().__init__(entries=entries, label="Material Bind Group Layout")


class MaterialBindGroup(BindGroup):
    def __init__(
        self,
        texture_view: wgpu.TextureView,
        sampler: wgpu.Sampler,
        index: int = BindGroupIndex.MATERIAL,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=MaterialBindIndex.TEXTURE, texture_view=texture_view
            ),
            wgpu.BindGroupEntry(binding=MaterialBindIndex.SAMPLER, sampler=sampler),
        ]

        super().__init__(
            entries=entries,
            layout=MaterialBindGroupLayout(),
            label="Sprite Bind Group",
            index=index,
        )
