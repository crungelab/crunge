from .resource import Resource
from .texture import TextureKit
from .material import MaterialKit

from .texture.sprite_atlas_kit import SpriteAtlasKit

class ResourceGroup:
    def __init__(self) -> None:
        self.texture_kit = TextureKit()
        self.texture_atlas_kit = SpriteAtlasKit()
        self.material_kit = MaterialKit()

    def add(self, resource: Resource) -> int:
        resource.add_to_group(self)