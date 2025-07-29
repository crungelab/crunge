from loguru import logger

from crunge import wgpu

from ...resource.model import ModelGroup

from . import Sprite


class SpriteGroup(ModelGroup[Sprite]):
    def __init__(self):
        super().__init__()
        self.is_dynamic_group = False

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        raise NotImplementedError("SpriteGroup.bind should be implemented in subclasses")