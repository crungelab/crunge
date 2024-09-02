from pathlib import Path

from loguru import logger

from crunge.engine import RectI

from .texture_loader_base import TextureLoaderBase

from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture


class TextureLoader(TextureLoaderBase[Texture]):
    def load(self, path: Path, name: str = None) -> Texture:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)

        if texture:= self.kit.get(name):
            return texture
        
        wgpu_texture, im_width, im_height = self.load_wgpu_texture([path])
        texture = Texture(name, RectI(0, 0, im_width, im_height), wgpu_texture)
        self.kit.add(texture)
        return texture