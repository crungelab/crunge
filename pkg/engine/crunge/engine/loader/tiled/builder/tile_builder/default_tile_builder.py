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

    def build(self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int,
            properties: dict):
        tmx_flip_flags = properties.get("flip_flags")
        flip_flags = self.translate_flip_flags(tmx_flip_flags)

        # ASSUMPTION: flip_flags arrives as the raw tmx.TileLayer.FlipFlag mask
        # for this tile instance (attribute name on the TileLayer tile binding
        # unconfirmed — likely `.flip_flags`), distinct from TilesetTile.
        properties["type"] = tile.class_name
        path = tile.image_path
        atlas = SpriteTextureLoader().load(path)

        sprite = self.context.sprites.get((tile_gid, flip_flags))
        if sprite is None:
            base = self.context.sprites.get((tile_gid, 0))
            if base is None:
                image_position = tile.image_position
                image_size = tile.image_size
                sprite_builder = CollidableSpriteBuilder()
                base = sprite_builder.build(
                    atlas,
                    Rect2i(image_position.x, image_position.y,
                        image_size.x, image_size.y),
                )
                self.context.sprites[(tile_gid, 0)] = base

            if flip_flags:
                #h = bool(flip_flags & tmx.TileLayer.FlipFlag.HORIZONTAL)
                #v = bool(flip_flags & tmx.TileLayer.FlipFlag.VERTICAL)
                #d = bool(flip_flags & tmx.TileLayer.FlipFlag.DIAGONAL)
                #sprite = base.mirror(h, v, d)
                #sprite = base.mirror(h, v)
                sprite = base.mirror(flip_flags)
                self.context.sprites[(tile_gid, flip_flags)] = sprite
            else:
                sprite = base

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)
    """
    def build(self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int, properties: dict):
        properties["type"] = tile.class_name
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
        flip_flags = properties.get("flip_flags")

        #logger.debug(f"tile_gid: {tile_gid}, path: {path}, pos: {image_position}, size: {image_size}")
        #logger.debug(f"sprites: {len(self.context.sprites)}")

        sprite = self.context.sprites[tile_gid]
        #logger.debug(f"sprite: {sprite}")

        if sprite is None:
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
            if flip_flags == tmx.TileLayer.FlipFlag.HORIZONTAL:
                sprite = sprite.mirror(True)
            else:
                self.context.sprites[tile_gid] = sprite

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)
    """

    """
    def build(self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int, properties: dict):
        properties["type"] = tile.class_name
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

        #logger.debug(f"tile_gid: {tile_gid}, path: {path}, pos: {image_position}, size: {image_size}")
        #logger.debug(f"sprites: {len(self.context.sprites)}")

        sprite = self.context.sprites[tile_gid]
        #logger.debug(f"sprite: {sprite}")

        if sprite is None:
            sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
            self.context.sprites[tile_gid] = sprite

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, sprite, properties)
        else:
            node = self.create_node(position, sprite, properties)

        if node is not None:
            self.layer.attach(node)
    """

    def create_node(self, position: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, vu=SpriteVu(), model=sprite)
        return node
