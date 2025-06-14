from enum import IntEnum

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


@klass.singleton
class CameraBGL(BindGroupLayout):
    class Index:
        CAMERA_UNIFORM = 0

    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=self.Index.CAMERA_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=entries)
        bind_group_layout = self.device.create_bind_group_layout(bgl_desc)
        super().__init__(bind_group_layout)


class CameraBindGroup(BindGroup):
    def __init__(self, uniform_buffer: wgpu.Buffer, uniform_buffer_size: int) -> None:
        bgl = CameraBGL()
        entries = [
            wgpu.BindGroupEntry(
                binding=bgl.Index.CAMERA_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Camera bind group",
            layout=bgl.get(),
            entries=entries,
        )

        bind_group = self.device.create_bind_group(bind_group_desc)
        super().__init__(bind_group)


@klass.singleton
class MaterialBGL(BindGroupLayout):
    class Index:
        SAMPLER = 0
        TEXTURE = 1
        MATERIAL_UNIFORM = 2

    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=self.Index.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=self.Index.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=self.Index.MATERIAL_UNIFORM,
                # visibility=wgpu.ShaderStage.FRAGMENT,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=entries)
        bind_group_layout = self.device.create_bind_group_layout(bgl_desc)
        super().__init__(bind_group_layout)


class MaterialBindGroup(BindGroup):
    def __init__(
        self,
        sampler: wgpu.Sampler,
        texture_view: wgpu.TextureView,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
    ) -> None:
        bgl = MaterialBGL()
        entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=bgl.Index.SAMPLER, sampler=sampler),
                wgpu.BindGroupEntry(
                    binding=bgl.Index.TEXTURE, texture_view=texture_view
                ),
                wgpu.BindGroupEntry(
                    binding=bgl.Index.MATERIAL_UNIFORM,
                    buffer=uniform_buffer,
                    size=uniform_buffer_size,
                ),
            ]
        )

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=bgl.get(),
            entries=entries,
        )

        bind_group = self.device.create_bind_group(bind_group_desc)
        super().__init__(bind_group)


@klass.singleton
class ModelBGL(BindGroupLayout):
    class Index:
        MODEL_UNIFORM = 0

    def __init__(self) -> None:
        model_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        model_bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=model_bgl_entries)
        bind_group_layout = self.device.create_bind_group_layout(model_bgl_desc)
        super().__init__(bind_group_layout)


class ModelBindGroup(BindGroup):
    def __init__(self, uniform_buffer: wgpu.Buffer, uniform_buffer_size: int) -> None:
        bgl = ModelBGL()
        entries = [
            wgpu.BindGroupEntry(
                binding=bgl.Index.MODEL_UNIFORM,
                buffer=uniform_buffer,
                size=uniform_buffer_size,
            ),
        ]

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model bind group",
            layout=bgl.get(),
            entries=entries,
        )

        bind_group = self.device.create_bind_group(bind_group_desc)

        super().__init__(bind_group)
