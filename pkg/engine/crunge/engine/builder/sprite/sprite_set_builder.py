from typing import TypeVar, Generic, Dict, List

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture

from ...resource.sprite.sprite_set import SpriteSet
from ...resource.sprite.sprite_set_kit import SpriteSetKit

from ...resource.texture.image_texture import ImageTexture

from ..resource_builder import ResourceBuilder
from ..texture.image_texture_builder import ImageTextureBuilder

T_Resource = TypeVar("T_Resource", bound=SpriteSet[ImageTexture])


class SpriteSetBuilder(ResourceBuilder[T_Resource], Generic[T_Resource]):
    def __init__(
        self,
        texture_builder=ImageTextureBuilder(),
        kit: SpriteSetKit = ResourceManager().sprite_set_kit,
    ) -> None:
        super().__init__(kit)
        self.texture_builder = texture_builder
