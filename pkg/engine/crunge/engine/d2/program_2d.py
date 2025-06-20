from typing import List

from loguru import logger
from jinja2 import BaseLoader, PackageLoader

from crunge import wgpu

from ..program import Program

from ..bindings import (
    GlobalBindGroupIndex,
    ViewportBindGroupLayout,
    ViewportBindIndex,
)

from .bindings import (
    BindGroupIndex,
    CameraBindIndex,
    SpriteBindIndex,
    ModelBindIndex,
)


class Program2D(Program):
    def __init__(self, template_loaders: List[BaseLoader] = []):
        template_loaders.append(PackageLoader("crunge.engine.resources.shaders", "d2"))
        super().__init__(template_loaders)
        self.template_dict = {
            "GlobalBindGroupIndex": GlobalBindGroupIndex,
            "BindGroupIndex": BindGroupIndex,
            "ViewportBindIndex": ViewportBindIndex,
            "CameraBindIndex": CameraBindIndex,
            "MaterialBindIndex": SpriteBindIndex,
            "ModelBindIndex": ModelBindIndex,
        }

    '''
    @property
    def viewport_bind_group_layout(self):
        return ViewportBindGroupLayout()

    @property
    def camera_bind_group_layout(self):
        return CameraBindGroupLayout()

    @property
    def material_bind_group_layout(self):
        return SpriteBindGroupLayout()

    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout()

    @property
    def bind_group_layouts(self) -> list[wgpu.BindGroupLayout]:
        bind_group_layouts = [
            self.viewport_bind_group_layout.get(),
            self.camera_bind_group_layout.get(),
            self.material_bind_group_layout.get(),
            self.model_bind_group_layout.get(),
        ]

        return bind_group_layouts
    '''