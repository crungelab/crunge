from typing import List

from loguru import logger
from jinja2 import BaseLoader, PackageLoader

from ..program import Program

from ..bindings import (
    BindGroupIndex,
    CameraBindIndex,
)

from .bindings_2d import (
    BindGroupIndex,
    SpriteBindIndex,
    ModelBindIndex,
)


class Program2D(Program):
    def __init__(self, template_loaders: List[BaseLoader] = []):
        template_loaders.append(PackageLoader("crunge.engine.resources.shaders", "d2"))
        super().__init__(template_loaders)
        self.template_dict = {
            "BindGroupIndex": BindGroupIndex,
            "BindGroupIndex": BindGroupIndex,
            "CameraBindIndex": CameraBindIndex,
            "MaterialBindIndex": SpriteBindIndex,
            "ModelBindIndex": ModelBindIndex,
        }
