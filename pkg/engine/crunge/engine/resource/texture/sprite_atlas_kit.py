from loguru import logger

from ..resource_kit import ResourceKit
from .sprite_atlas import SpriteAtlas

class SpriteAtlasKit(ResourceKit[SpriteAtlas]):
    def __init__(self):
        super().__init__()
