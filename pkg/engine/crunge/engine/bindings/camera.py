from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..resource.bind_group import BindGroupLayout, BindGroup

from . import BindGroupIndex


class CameraBindIndex:
    CAMERA_UNIFORM = 0
    VIEWPORT_UNIFORM = 1
    SNAPSHOT_TEXTURE = 2
    SNAPSHOT_SAMPLER = 3


@klass.singleton
class CameraBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=CameraBindIndex.CAMERA_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=CameraBindIndex.VIEWPORT_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=CameraBindIndex.SNAPSHOT_TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=CameraBindIndex.SNAPSHOT_SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
        ]
        super().__init__(entries=entries, label="Camera Bind Group Layout")


class CameraBindGroup(BindGroup):
    def __init__(
        self,
        camera_uniform_buffer: wgpu.Buffer,
        camera_uniform_buffer_size: int,
        viewport_uniform_buffer: wgpu.Buffer,
        viewport_uniform_buffer_size: int,
        texture_view: wgpu.TextureView,
        sampler: wgpu.Sampler,
        index: int = BindGroupIndex.CAMERA,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=CameraBindIndex.CAMERA_UNIFORM,
                buffer=camera_uniform_buffer,
                size=camera_uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=CameraBindIndex.VIEWPORT_UNIFORM,
                buffer=viewport_uniform_buffer,
                size=viewport_uniform_buffer_size,
            ),
            wgpu.BindGroupEntry(
                binding=CameraBindIndex.SNAPSHOT_TEXTURE, texture_view=texture_view
            ),
            wgpu.BindGroupEntry(binding=CameraBindIndex.SNAPSHOT_SAMPLER, sampler=sampler),
        ]

        super().__init__(
            entries=entries, layout=CameraBindGroupLayout(), label="Camera Bind Group", index=index
        )
