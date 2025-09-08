from loguru import logger
import glm

from crunge import tmx

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu, SpriteLayer
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
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
    
    def build(self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int, properties: dict):
        properties["type"] = tile.class_name  # TODO:?
        #logger.debug(f"process_tile: {position}, {image}, {properties}")
        path = tile.image_path
        atlas = SpriteTextureLoader().load(path)
        # logger.debug(f"atlas: {atlas}")
        sprite_builder = CollidableSpriteBuilder()
        image_position = tile.image_position
        tx = image_position.x
        ty = image_position.y
        image_size = tile.image_size
        tw = image_size.x
        th = image_size.y

        logger.debug(f"tile_gid: {tile_gid}, path: {path}, pos: {image_position}, size: {image_size}")
        logger.debug(f"sprites: {len(self.context.sprites)}")
        sprite = self.context.sprites[tile_gid]
        if sprite is None:
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
            self.context.sprites[tile_gid] = sprite
        '''
        sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
        '''
        #logger.debug(f"sprite: {sprite}")

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)

    def create_node(self, position: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, vu=SpriteVu(), model=sprite)
        return node

