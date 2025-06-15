from loguru import logger
from jinja2 import PackageLoader

from crunge import wgpu

from ..program import Program
from .bindings_2d import (
    BindGroupIndex,
    CameraBindIndex,
    MaterialBindIndex,
    ModelBindIndex,
    CameraBGL,
    MaterialBGL,
    ModelBGL,
)


class Program2D(Program):
    def __init__(self):
        super().__init__([PackageLoader("crunge.engine.d2", "templates")])
        self.template_dict = {
            "BindGroupIndex": BindGroupIndex,
            "CameraBindIndex": CameraBindIndex,
            "MaterialBindIndex": MaterialBindIndex,
            "ModelBindIndex": ModelBindIndex,
        }

    @property
    def camera_bind_group_layout(self):
        return CameraBGL().get()

    @property
    def material_bind_group_layout(self):
        return MaterialBGL().get()

    @property
    def model_bind_group_layout(self):
        return ModelBGL().get()

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
