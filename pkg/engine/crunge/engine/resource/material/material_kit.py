from loguru import logger

from ..resource_kit import ResourceKit
from .material import Material


class MaterialKit(ResourceKit[Material]):
    def __init__(self):
        super().__init__()
