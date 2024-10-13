from pathlib import Path

from loguru import logger

from ..math import Rect2i
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture

from .texture_loader_base import TextureLoaderBase


class TextureLoader(TextureLoaderBase[Texture]):
    def load(self, path: Path, name: str = None) -> Texture:
        path = ResourceManager().resolve_path(path)

        if texture:= self.kit.get_by_path(path):
            return texture
        
        wgpu_texture, im_width, im_height = self.load_wgpu_texture([path])
        texture = Texture(wgpu_texture, Rect2i(0, 0, im_width, im_height)).set_name(name).set_path(path)
        self.kit.add(texture)
        return texture