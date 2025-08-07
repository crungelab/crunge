from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture, TextureKit
from ...resource.image import Image

from ...resource.sprite.sprite_atlas import SpriteAtlas
from ...resource.texture.image_texture import ImageTexture
from ..texture.image_texture_builder import ImageTextureBuilder


class SpriteAtlasBuilder(ImageTextureBuilder):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, image: Image) -> ImageTexture:
        wgpu_texture = self.build_wpgu_texture(image)
        texture = ImageTexture(wgpu_texture, image.size, image)
        atlas = SpriteAtlas(texture)
        return atlas
