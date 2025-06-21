from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ....resource.bind_group import BindGroupLayout, BindGroup

from .. import BindGroupIndex


class ShapeBindIndex:
    MATERIAL_UNIFORM = 0


@klass.singleton
class ShapeBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=ShapeBindIndex.MATERIAL_UNIFORM,
                # visibility=wgpu.ShaderStage.FRAGMENT,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        super().__init__(entries=entries, label="Shape Bind Group Layout")


class ShapeBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.MATERIAL,
    ) -> None:
        entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=ShapeBindIndex.MATERIAL_UNIFORM,
                    buffer=uniform_buffer,
                    size=uniform_buffer_size,
                ),
            ]
        )

        super().__init__(
            entries=entries,
            layout=ShapeBindGroupLayout(),
            label="Shape Bind Group",
            index=index,
        )
