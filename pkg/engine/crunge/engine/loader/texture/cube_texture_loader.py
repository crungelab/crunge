from typing import List

from pathlib import Path

from loguru import logger

from crunge.engine.math import Rect2i

from .texture_loader_base import TextureLoaderBase

from ...resource.texture.cube_texture import CubeTexture


class CubeTextureLoader(TextureLoaderBase):
    def __init__(self) -> None:
        super().__init__()

    def load(self, paths: List[Path], name: str = "") -> CubeTexture:
        details = self.load_wgpu_texture(paths)
        return CubeTexture(details.texture, Rect2i(0, 0, details.width, details.height)).set_name(name)