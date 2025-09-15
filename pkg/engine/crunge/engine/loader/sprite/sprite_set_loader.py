from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_set import SpriteSet

from ..resource_loader import ResourceLoader

T_Resource = TypeVar("T_Resource", bound=SpriteSet)

class SpriteSetLoader(ResourceLoader[T_Resource], Generic[T_Resource]):
    def __init__(self) -> None:
        super().__init__(kit=ResourceManager().sprite_set_kit)