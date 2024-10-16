from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ..program import Program
from ..resource.bind_group_layout import BindGroupLayout


@klass.singleton
class CameraBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(camera_bgl_entries), entries=camera_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)


class LightBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        light_bgl_entries = [
            # Ambient Light
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            # Light
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        light_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(light_bgl_entries), entries=light_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(light_bgl_desc)
        logger.debug(f"light_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)


@klass.singleton
class MaterialBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        material_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=2,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        material_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(material_bgl_entries), entries=material_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(material_bgl_desc)
        logger.debug(f"material_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)


@klass.singleton
class ModelBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        model_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        model_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(model_bgl_entries), entries=model_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(model_bgl_desc)
        logger.debug(f"model_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)


class Program3D(Program):
    def __init__(self):
        super().__init__()

    @property
    def camera_bind_group_layout(self):
        return CameraBindGroupLayout().get()

    @property
    def light_bind_group_layout(self):
        return LightBindGroupLayout().get()
    
    @property
    def material_bind_group_layout(self):
        return MaterialBindGroupLayout().get()

    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout().get()

    @property
    def bind_group_layouts(self) -> list[wgpu.BindGroupLayout]:
        bind_group_layouts = wgpu.BindGroupLayouts(
            [
                self.camera_bind_group_layout,
                self.light_bind_group_layout,
                self.material_bind_group_layout,
                self.model_bind_group_layout,
            ]
        )
        return bind_group_layouts
