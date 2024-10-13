from typing import List

from pathlib import Path

from loguru import logger

from crunge.engine.math import Rect2i

from .texture_loader_base import TextureLoaderBase

from ..resource.cube_texture import CubeTexture


class CubeTextureLoader(TextureLoaderBase):
    def __init__(self) -> None:
        super().__init__()

    def load(self, paths: List[Path], name: str = "") -> CubeTexture:
        texture, im_width, im_height = self.load_wgpu_texture(paths)
        return CubeTexture(texture, Rect2i(0, 0, im_width, im_height)).set_name(name)