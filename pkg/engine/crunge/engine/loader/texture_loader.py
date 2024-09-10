from pathlib import Path

from loguru import logger

from crunge.engine import RectI

from .texture_loader_base import TextureLoaderBase

from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture


class TextureLoader(TextureLoaderBase[Texture]):
    def load(self, path: Path, name: str = None) -> Texture:
        path = ResourceManager().resolve_path(path)

        if texture:= self.kit.get_by_path(path):
            return texture
        
        wgpu_texture, im_width, im_height = self.load_wgpu_texture([path])
        texture = Texture(wgpu_texture, RectI(0, 0, im_width, im_height)).set_name(name).set_path(path)
        self.kit.add(texture)
        return texture