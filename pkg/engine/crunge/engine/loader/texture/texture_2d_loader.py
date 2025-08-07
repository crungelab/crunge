from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path

from loguru import logger
import glm

from ...resource.resource_manager import ResourceManager
from ...resource.texture import Texture2D

from .texture_loader import TextureLoader

T_Texture = TypeVar("T_Texture", bound=Texture2D)

#class Texture2DLoader(TextureLoaderBase[Texture2D]):
class Texture2DLoader(TextureLoader[T_Texture], Generic[T_Texture]):
    def load(self, path: Path, name: str = None) -> T_Texture:
        path = ResourceManager().resolve_path(path)

        #if texture:= self.kit.get_by_path(path):
        if texture:= self.kit.get_by_name(name) or self.kit.get_by_path(path):
            return texture

        details = self.load_wgpu_texture([path])
        texture = Texture2D(details.texture, glm.ivec2(details.width, details.height)).set_name(name).set_path(path)
        self.kit.add(texture)
        return texture