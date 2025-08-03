from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path

from loguru import logger
import glm

from ...resource.resource_manager import ResourceManager
from ...resource.texture import Texture2dArray

from .texture_loader_base import TextureLoaderBase

T_Texture = TypeVar("T_Texture", bound=Texture2dArray)

class Texture2dArrayLoader(TextureLoaderBase[T_Texture], Generic[T_Texture]):
    def load(self, paths: List[Path], name: str = None) -> T_Texture:
        #if texture:= self.kit.get_by_path(path):
        #if texture:= self.kit.get_by_name(name) or self.kit.get_by_path(path):
        if texture:= self.kit.get_by_name(name):
            return texture

        paths = [ResourceManager().resolve_path(path) for path in paths]

        details = self.load_wgpu_texture(paths)
        texture = Texture2dArray(details.texture, glm.ivec3(details.width, details.height, details.depth)).set_name(name)
        self.kit.add(texture)
        return texture