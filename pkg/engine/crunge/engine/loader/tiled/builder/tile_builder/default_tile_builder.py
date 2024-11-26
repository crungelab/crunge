from loguru import logger
import glm

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from .tile_builder import TileBuilder


class DefaultTileBuilder(TileBuilder):
    def build(self, position: glm.vec2, image, properties):
        logger.debug(f"process_tile: {position}, {image}, {properties}")
        path = image[0]
        atlas = ImageTextureLoader().load(path)
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

        vu = SpriteVu(sprite).create()
        size = glm.vec2(sprite.width, sprite.height)
        node = Node2D(position, size=size, vu=vu, model=sprite)
        #self.context.scene.attach(node)
        self.context.layer.attach(node)
