from loguru import logger

from ....resource.material import MaterialGroup

from .. import Sprite


class SpriteGroup(MaterialGroup[Sprite]):
    def __init__(self):
        super().__init__()
        self.is_buffered_group = False
