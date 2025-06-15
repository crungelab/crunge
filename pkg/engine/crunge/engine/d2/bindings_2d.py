from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..resource.bind_group import BindGroupLayout, BindGroup


class BindGroupIndex:
    # VIEWPORT = 0
    CAMERA = 0
    # LIGHT = auto()
    MATERIAL = 1
    MODEL = 2


class CameraBindIndex:
    CAMERA_UNIFORM = 0


@klass.singleton
class CameraBGL(BindGroupLayout):
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
            entries=entries, layout=CameraBGL(), label="Camera Bind Group", index=index
        )


class MaterialBindIndex:
    MATERIAL_UNIFORM = 0
    SAMPLER = 1
    TEXTURE = 2


@klass.singleton
class MaterialBGL(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=MaterialBindIndex.MATERIAL_UNIFORM,
                # visibility=wgpu.ShaderStage.FRAGMENT,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=MaterialBindIndex.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=MaterialBindIndex.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
        ]

        super().__init__(entries=entries, label="Material Bind Group Layout")


class MaterialBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        sampler: wgpu.Sampler,
        texture_view: wgpu.TextureView,
        index: int = BindGroupIndex.MATERIAL,
    ) -> None:
        entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=MaterialBindIndex.MATERIAL_UNIFORM,
                    buffer=uniform_buffer,
                    size=uniform_buffer_size,
                ),
                wgpu.BindGroupEntry(binding=MaterialBindIndex.SAMPLER, sampler=sampler),
                wgpu.BindGroupEntry(
                    binding=MaterialBindIndex.TEXTURE, texture_view=texture_view
                ),
            ]
        )

        super().__init__(
            entries=entries, layout=MaterialBGL(), label="Material Bind Group", index=index
        )


class ModelBindIndex:
    MODEL_UNIFORM = 0

@klass.singleton
class ModelBGL(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        super().__init__(entries=entries, label="Model Bind Group Layout")


class ModelBindGroup(BindGroup):
    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        index: int = BindGroupIndex.MODEL,
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        super().__init__(
            entries=entries, layout=ModelBGL(), label="Model Bind Group", index=index
        )
