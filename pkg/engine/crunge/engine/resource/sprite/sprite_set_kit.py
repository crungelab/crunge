from loguru import logger

from ..resource_kit import ResourceKit
from .sprite_set import SpriteSet

class SpriteSetKit(ResourceKit[SpriteSet]):
    def __init__(self):
        super().__init__()
