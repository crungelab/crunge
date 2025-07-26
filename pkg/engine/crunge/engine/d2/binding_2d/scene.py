from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...binding import BindGroupLayout, BindGroup

from . import BindGroupIndex


class SceneBindIndex:
    CAMERA_UNIFORM = 0


@klass.singleton
class SceneBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=SceneBindIndex.CAMERA_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries=entries, label="Scene Bind Group Layout")


class SceneBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.SCENE,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=SceneBindIndex.CAMERA_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(
            entries=entries, layout=SceneBindGroupLayout(), label="Scene Bind Group", index=index
        )
