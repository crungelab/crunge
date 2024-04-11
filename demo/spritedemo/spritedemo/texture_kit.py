from typing import Dict
from pathlib import Path

import imageio as iio
from loguru import logger

from crunge.core import klass
from crunge import wgpu
from crunge.wgpu import utils
from .texture_kit_base import TextureKitBase
from .texture import Texture
from .texture_atlas import TextureAtlas

@klass.singleton
class TextureKit(TextureKitBase):
    def __init__(self):
        super().__init__()


    def load(self, path: Path) -> Texture:
        if path in self.textures:
            return self.textures[path]
        wgpu_texture, width, height = self.load_wgpu_texture(path)
        texture = Texture(wgpu_texture, 0, 0, width, height)
        self.textures[path] = texture
        return texture
