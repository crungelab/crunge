from loguru import logger

from ...resource.model import ModelGroup

from . import Sprite


class SpriteGroup(ModelGroup[Sprite]):
    def __init__(self):
        super().__init__()
        self.is_dynamic_group = False
