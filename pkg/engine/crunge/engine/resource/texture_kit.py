from typing import Dict
from pathlib import Path

import glm
from loguru import logger

from crunge.core import klass

from .. import RectI
from .texture_kit_base import TextureKitBase
from .texture import Texture


@klass.singleton
class TextureKit(TextureKitBase):
    def __init__(self):
        super().__init__()


    def load(self, path: Path) -> Texture:
        if path in self.textures:
            return self.textures[path]
        wgpu_texture, width, height = self.load_wgpu_texture(path)
        #texture = Texture(path, wgpu_texture, glm.ivec2(0, 0), glm.ivec2(width, height))
        texture = Texture(path, RectI(0, 0, width, height), wgpu_texture)
        self.textures[path] = texture
        return texture
