from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_set import SpriteSet

from ..resource_loader import ResourceLoader


class SpriteSetLoader(ResourceLoader[SpriteSet]):
    def __init__(self) -> None:
        super().__init__(kit=ResourceManager().sprite_set_kit)
