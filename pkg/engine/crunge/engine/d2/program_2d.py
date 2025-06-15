from loguru import logger

from crunge import wgpu

from ..program import Program
from .bindings_2d import CameraBGL, MaterialBGL, ModelBGL


class Program2D(Program):
    def __init__(self):
        super().__init__()

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
