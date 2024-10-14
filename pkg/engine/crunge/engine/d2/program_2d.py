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

from crunge import wgpu

from ..program import Program


class Program2D(Program):
    _camera_bindgroup_layout: wgpu.BindGroupLayout = None
    _material_bindgroup_layout: wgpu.BindGroupLayout = None
    _model_bindgroup_layout: wgpu.BindGroupLayout = None
    #_bind_group_layouts: list[wgpu.BindGroupLayout] = None

    def __init__(self):
        super().__init__()

    @property
    def camera_bindgroup_layout(self):
        if self._camera_bindgroup_layout is None:
            self.create_camera_bindgroup_layout()
        return self._camera_bindgroup_layout
    
    @property
    def material_bindgroup_layout(self):
        if self._material_bindgroup_layout is None:
            self.create_material_bindgroup_layout()
        return self._material_bindgroup_layout
    
    @property
    def model_bindgroup_layout(self):
        if self._model_bindgroup_layout is None:
            self.create_model_bindgroup_layout()
        return self._model_bindgroup_layout
    
    @property
    def bind_group_layouts(self) -> list[wgpu.BindGroupLayout]:
        bind_group_layouts = wgpu.BindGroupLayouts(
            [self.camera_bindgroup_layout, self.material_bindgroup_layout, self.model_bindgroup_layout]
        )
        return bind_group_layouts

    def create_camera_bindgroup_layout(self):
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(camera_bgl_entries), entries=camera_bgl_entries
        )
        self._camera_bindgroup_layout = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {self._camera_bindgroup_layout}")

    def create_material_bindgroup_layout(self):
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
        self._material_bindgroup_layout = self.device.create_bind_group_layout(material_bgl_desc)
        logger.debug(f"material_bgl: {self._material_bindgroup_layout}")

    def create_model_bindgroup_layout(self):
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
        self._model_bindgroup_layout = self.device.create_bind_group_layout(model_bgl_desc)
        logger.debug(f"model_bgl: {self._model_bindgroup_layout}")
