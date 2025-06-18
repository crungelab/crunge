from loguru import logger
from jinja2 import PackageLoader

from crunge import wgpu

from ..program import Program
from .bindings import (
    BindGroupIndex,
    CameraBindIndex,
    SpriteBindIndex,
    ModelBindIndex,
    CameraBindGroupLayout,
    SpriteBindGroupLayout,
    ModelBindGroupLayout,
)


class Program2D(Program):
    def __init__(self):
        super().__init__([PackageLoader("crunge.engine.d2", "templates")])
        self.template_dict = {
            "BindGroupIndex": BindGroupIndex,
            "CameraBindIndex": CameraBindIndex,
            "MaterialBindIndex": SpriteBindIndex,
            "ModelBindIndex": ModelBindIndex,
        }

    @property
    def camera_bind_group_layout(self):
        return CameraBindGroupLayout().get()

    @property
    def material_bind_group_layout(self):
        return SpriteBindGroupLayout().get()

    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout().get()

    @property
    def bind_group_layouts(self) -> list[wgpu.BindGroupLayout]:
        bind_group_layouts = wgpu.BindGroupLayouts(
            [
                self.camera_bind_group_layout,
                self.material_bind_group_layout,
                self.model_bind_group_layout,
            ]
        )
        return bind_group_layouts
