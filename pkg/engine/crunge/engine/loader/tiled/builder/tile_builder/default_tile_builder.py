from loguru import logger
import glm

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu, SpriteLayer
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
#from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.loader.texture.sprite_texture_loader import SpriteTextureLoader

from ..builder_context import BuilderContext

from .tile_builder import TileBuilder


class DefaultTileBuilder(TileBuilder):
    def __init__(self, context: BuilderContext, create_node_cb=None):
        super().__init__(context)
        self.create_node_cb = create_node_cb

    @property
    def layer(self) -> SpriteLayer:
        return self.context.layer
    
    def build(self, position: glm.vec2, image: tuple, properties: dict):
        logger.debug(f"process_tile: {position}, {image}, {properties}")
        path = image[0]
        atlas = SpriteTextureLoader().load(path)
        # logger.debug(f"atlas: {atlas}")
        sprite_builder = CollidableSpriteBuilder()
        rect = image[1]
        if rect:
            tx, ty, tw, th = rect
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
        else:
            sprite = sprite_builder.build(
                atlas, Rect2i(0, 0, atlas.width, atlas.height)
            )

        logger.debug(f"sprite: {sprite}")

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)

    def create_node(self, position: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, vu=SpriteVu(), model=sprite)
        return node

