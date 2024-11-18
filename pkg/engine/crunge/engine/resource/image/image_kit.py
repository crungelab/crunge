from loguru import logger

from ..resource_kit import ResourceKit
from .image import Image


class ImageKit(ResourceKit[Image]):
    def __init__(self):
        super().__init__()
