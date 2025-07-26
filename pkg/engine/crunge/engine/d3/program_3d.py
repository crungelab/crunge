from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ..program import Program
from ..binding.bind_group_layout import BindGroupLayout
from ..binding import SceneBindGroupLayout
'''
@klass.singleton
class CameraBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries, label="CameraBindGroupLayout")
'''

class LightBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
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
        super().__init__(entries, label="LightBindGroupLayout")


@klass.singleton
class MaterialBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        material_bgl_entries = [
            # Sampler
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            # Texture
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            # Material
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
        super().__init__(bind_group_layout, label="MaterialBindGroupLayout")


@klass.singleton
class ModelBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]
        super().__init__(entries, label="ModelBindGroupLayout")


class Program3D(Program):
    def __init__(self):
        super().__init__()

    @property
    def camera_bind_group_layout(self):
        return SceneBindGroupLayout().get()

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
