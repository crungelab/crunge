from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...resource.bind_group import BindGroupLayout, BindGroup

from . import BindGroupIndex


class CameraBindIndex:
    CAMERA_UNIFORM = 0


@klass.singleton
class CameraBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=CameraBindIndex.CAMERA_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries=entries, label="Camera Bind Group Layout")


class CameraBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.CAMERA,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=CameraBindIndex.CAMERA_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(
            entries=entries, layout=CameraBindGroupLayout(), label="Camera Bind Group", index=index
        )
