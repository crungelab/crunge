from loguru import logger
import glm

from crunge import tmx

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu, SpriteLayer
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.sprite_texture_loader import SpriteTextureLoader

from .tile_builder import TileBuilder


class DefaultTileBuilder(TileBuilder):
    def __init__(self, create_node_cb=None):
        super().__init__()
        self.create_node_cb = create_node_cb

    @property
    def layer(self) -> SpriteLayer:
        return self.context.current_graph_layer

    def build(self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int, properties: dict):
        properties["type"] = tile.class_name
        path = tile.image_path
        atlas = SpriteTextureLoader().load(path)
        sprite_builder = CollidableSpriteBuilder()
        image_position = tile.image_position
        tx = image_position.x
        ty = image_position.y
        image_size = tile.image_size
        tw = image_size.x
        th = image_size.y

        sprite = self.context.sprites[tile_gid]
        if sprite is None:
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
            self.context.sprites[tile_gid] = sprite

        # sprite.rect is the cropped collision_rect (absolute atlas coords) —
        # its center no longer matches the full tile's center, so compute the
        # drift and shift the node position to compensate.
        tile_center = glm.vec2(tx + tw / 2.0, ty + th / 2.0)
        crop_center = glm.vec2(
            sprite.rect.x + sprite.rect.width / 2.0,
            sprite.rect.y + sprite.rect.height / 2.0,
        )
        pixel_offset = crop_center - tile_center          # source-image pixel space, Y-down
        scene_offset = glm.vec2(pixel_offset.x, -pixel_offset.y) / sprite.ppu  # -> units, Y-up

        position = position + scene_offset

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)

    '''
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
        #logger.debug(f"sprite: {sprite}")

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)
    '''

    def create_node(self, position: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, vu=SpriteVu(), model=sprite)
        return node

