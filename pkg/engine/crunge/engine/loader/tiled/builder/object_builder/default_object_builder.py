from loguru import logger
import glm

from crunge import tmx

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.sprite.sprite_sampler import DefaultSpriteSampler
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.sprite_texture_loader import SpriteTextureLoader

from .object_builder import ObjectBuilder


class DefaultObjectBuilder(ObjectBuilder):
    def __init__(self, create_node_cb=None):
        super().__init__()
        self.create_node_cb = create_node_cb

    def build(self, obj: tmx.Object):
        map = self.map
        properties = obj.properties

        tile = map.get_tile(obj.get_tile_id())
        if tile is None:
            return

        properties["type"] = tile.class_name

        image_path = tile.image_path
        atlas = SpriteTextureLoader().load(image_path)
        atlas_size = glm.vec2(atlas.size.xy)

        aabb = obj.get_aabb()
        width = aabb.width
        height = aabb.height
        size = glm.vec2(width, height)

        x = aabb.left
        y = self.context.size.y - aabb.top
        lower_left = glm.vec2(x, y) / self.ppu

        rotation = -glm.radians(obj.rotation)

        # Build the sprite first — center/scale below depend on the actual cropped rect
        sprite_builder = CollidableSpriteBuilder()
        color = glm.vec4(1.0, 1.0, 1.0, self.context.opacity)
        sprite = sprite_builder.build(
            atlas,
            Rect2i(0, 0, atlas_size.x, atlas_size.y),
            sampler=DefaultSpriteSampler(),
            color=color,
        )
        
        # Nominal half-size (Tiled's authored center, in local units)
        center = size / 2.0 / self.ppu

        # Drift between crop center and full-atlas center, same convention as
        # DefaultTileBuilder's crop-offset fix (pixel space Y-down -> scene Y-up)
        atlas_center = atlas_size / 2.0
        crop_center = glm.vec2(
            sprite.rect.x + sprite.rect.width / 2.0,
            sprite.rect.y + sprite.rect.height / 2.0,
        )
        pixel_offset = (crop_center  - atlas_center)
        scene_offset = glm.vec2(pixel_offset.x, -pixel_offset.y) / sprite.ppu

        rotated_offset = glm.rotate(center + scene_offset, rotation)
        
        position = lower_left + rotated_offset
        position.y = position.y + self.context.map.tile_size.y / self.ppu

        #scale = glm.vec2(width, height) / glm.vec2(sprite.rect.size)
        scale = size / glm.vec2(atlas.size.xy)

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, rotation, scale, sprite, properties)
        else:
            node = self.create_node(position, rotation, scale, sprite, properties)

        if node is not None:
            self.context.current_graph_layer.attach(node)

    '''
    def build(self, obj: tmx.Object):
        map = self.map
        properties = obj.properties

        # Load the texture atlas
        tile_id = obj.get_tile_id()
        logger.debug(f"tile_id: {tile_id}")

        tile = map.get_tile(obj.get_tile_id())
        logger.debug(f"tile: {tile}")
        if tile is None:
            return

        properties["type"] = tile.class_name  # TODO:?

        image_path = tile.image_path
        atlas = SpriteTextureLoader().load(image_path)
        atlas_size = glm.vec2(atlas.size.xy)

        aabb = obj.get_aabb()
        width = aabb.width
        height = aabb.height

        size = glm.vec2(width, height)

        # Calculate half dimensions for centering
        center = size / 2.0 / self.ppu

        logger.debug(f"center: {center}")

        x = aabb.left
        y = self.context.size.y - aabb.top
        lower_left = glm.vec2(x, y) / self.ppu
        logger.debug(f"lower_left: {lower_left}")

        # Handle rotation in radians
        rotation = -glm.radians(obj.rotation)
        logger.debug(f"rotation: {rotation}")

        rotated_offset = glm.rotate(center, rotation)
        logger.debug(f"rotated_offset: {rotated_offset}")

        position = lower_left + rotated_offset
        position.y = position.y + self.context.map.tile_size.y / self.ppu
        logger.debug(f"position: {position}")

        # Calculate scale
        scale = glm.vec2(width / atlas_size.x, height / atlas_size.y)
        sampler = DefaultSpriteSampler()

        # Build the sprite
        sprite_builder = CollidableSpriteBuilder()
        color = glm.vec4(1.0, 1.0, 1.0, self.context.opacity)
        sprite = sprite_builder.build(
            atlas,
            Rect2i(0, 0, atlas_size.x, atlas_size.y),
            sampler=sampler,
            color=color,
        )

        logger.debug(f"sprite: {sprite}")

        if self.create_node_cb is not None:
            node = self.create_node_cb(position, rotation, scale, sprite, properties)
        else:
            node = self.create_node(position, rotation, scale, sprite, properties)

        # Attach the node to the appropriate layer
        if node is not None:
            self.context.current_graph_layer.attach(node)
    '''

    def create_node(
        self,
        position: glm.vec2,
        rotation: float,
        scale: glm.vec2,
        sprite: Sprite,
        properties: dict,
    ):
        node = Node2D(position, rotation, scale, vu=SpriteVu(), model=sprite)
        return node
