from typing import List

from loguru import logger
from jinja2 import BaseLoader, PackageLoader

from ..program import Program

from ..binding import (
    BindGroupIndex,
    SceneBindIndex,
)

from .binding_2d import (
    BindGroupIndex,
    SpriteBindIndex,
    ModelBindIndex,
    NodeBindIndex,
)


class Program2D(Program):
    def __init__(self, template_loaders: List[BaseLoader] = []):
        template_loaders.append(PackageLoader("crunge.engine.resources.shaders", "d2"))
        super().__init__(template_loaders)
        self.template_dict = {
            "BindGroupIndex": BindGroupIndex,
            "SceneBindIndex": SceneBindIndex,
            "MaterialBindIndex": SpriteBindIndex,
            "ModelBindIndex": ModelBindIndex,
            "NodeBindIndex": NodeBindIndex,
        }
