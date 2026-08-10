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

    def build(
        self, position: glm.vec2, tile: tmx.TilesetTile, tile_gid: int, properties: dict
    ):
        tmx_flip_flags = properties.get("flip_flags")
        flip_flags = self.translate_flip_flags(tmx_flip_flags)

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
                    Rect2i(
                        image_position.x, image_position.y, image_size.x, image_size.y
                    ),
                )
                self.context.sprites[(tile_gid, 0)] = base

            if flip_flags:
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

    def create_node(self, position: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, vu=SpriteVu(), model=sprite)
        return node
