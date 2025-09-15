from ...resource.resource_manager import ResourceManager
from ...resource.image import Image

from ...resource.sprite.sprite_atlas import SpriteAtlas
from ..texture.sprite_texture_builder import SpriteTextureBuilder
from .sprite_set_builder import SpriteSetBuilder


class SpriteAtlasBuilder(SpriteSetBuilder[SpriteAtlas]):
    def __init__(self, kit=ResourceManager().sprite_set_kit) -> None:
        super().__init__(texture_builder=SpriteTextureBuilder(), kit=kit)

    def build(self, image: Image) -> SpriteAtlas:
        texture = self.texture_builder.build(image)
        atlas = SpriteAtlas(texture)
        return atlas
