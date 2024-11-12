from pathlib import Path

from loguru import logger

from ..math import Rect2i
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture

from .texture_loader_base import TextureLoaderBase


class TextureLoader(TextureLoaderBase[Texture]):
    def load(self, path: Path, name: str = None) -> Texture:
        path = ResourceManager().resolve_path(path)

        #if texture:= self.kit.get_by_path(path):
        if texture:= self.kit.get_by_name(name) or self.kit.get_by_path(path):
            return texture

        details = self.load_wgpu_texture([path])
        texture = Texture(details.texture, Rect2i(0, 0, details.width, details.height)).set_name(name).set_path(path)
        self.kit.add(texture)
        return texture