from loguru import logger

from ..resource_kit import ResourceKit
from .model import Model


class ModelKit(ResourceKit[Model]):
    def __init__(self):
        super().__init__()
