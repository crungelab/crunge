from loguru import logger

from crunge.core import klass

from .resource_kit import ResourceKit
from .texture import Texture


@klass.singleton
class TextureKit(ResourceKit[Texture]):
    def __init__(self):
        super().__init__()
