from loguru import logger

from crunge import wgpu

from ...resource.model import ModelGroup

from .sprite import Sprite, SpriteMembership


class SpriteGroup(ModelGroup[Sprite]):
    def __init__(self):
        super().__init__()
        self.is_dynamic_group = False

    def create_membership(self, sprite: Sprite) -> SpriteMembership:
        raise NotImplementedError("SpriteGroup.create_membership should be implemented in subclasses")
    
    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        raise NotImplementedError("SpriteGroup.bind should be implemented in subclasses")