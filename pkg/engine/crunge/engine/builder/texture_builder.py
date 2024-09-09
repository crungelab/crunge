from pathlib import Path

from loguru import logger

from crunge.engine import RectI

from .texture_builder_base import TextureBuilderBase

from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture


class TextureBuilder(TextureBuilderBase[Texture]):
    def load(self, path: Path, name: str = None) -> Texture:
        path = ResourceManager().resolve_path(path)

        if texture:= self.kit.get_by_path(path):
            return texture
        
        wgpu_texture, im_width, im_height = self.load_wgpu_texture([path])
        texture = Texture(RectI(0, 0, im_width, im_height), wgpu_texture).set_name(name).set_path(path)
        self.kit.add(texture)
        return texture