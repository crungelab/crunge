from loguru import logger

from .resource_kit import ResourceKit
from .texture import Texture


class TextureKit(ResourceKit[Texture]):
    def __init__(self):
        super().__init__()
