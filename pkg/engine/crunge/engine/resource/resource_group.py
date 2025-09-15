from .resource import Resource
from .texture import TextureKit
from .material import MaterialKit

from .sprite.sprite_set_kit import SpriteSetKit

class ResourceGroup:
    def __init__(self) -> None:
        self.texture_kit = TextureKit()
        self.texture_array_kit = TextureKit()
        self.sprite_set_kit = SpriteSetKit()
        self.material_kit = MaterialKit()

    def add(self, resource: Resource) -> int:
        resource.add_to_group(self)