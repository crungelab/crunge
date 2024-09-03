from loguru import logger

from .resource_kit import ResourceKit
from .texture_atlas import TextureAtlas

class TextureAtlasKit(ResourceKit[TextureAtlas]):
    def __init__(self):
        super().__init__()
