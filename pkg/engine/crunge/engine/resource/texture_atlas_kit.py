from loguru import logger

from crunge.core import klass

from .resource_kit import ResourceKit
from .texture_atlas import TextureAtlas

@klass.singleton
class TextureAtlasKit(ResourceKit[TextureAtlas]):
    def __init__(self):
        super().__init__()
