from loguru import logger
import glm
from pytmx import TiledObject

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.sprite.sprite_sampler import DefaultSpriteSampler
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from ..builder_context import BuilderContext
from .object_builder import ObjectBuilder


class DefaultObjectBuilder(ObjectBuilder):
    def __init__(self, context: BuilderContext, create_node_cb=None):
        super().__init__(context)
        self.create_node_cb = create_node_cb

    def build(self, obj: TiledObject):
        properties = obj.properties
        # Check if the object is a polygon or line
        if hasattr(obj, "points"):
            # Handle polygons or lines if needed
            #pass
            raise NotImplementedError("Polygon or line objects are not supported")

        elif obj.image:
            # Load the texture atlas
            image = obj.image
            path = image[0]
            atlas = ImageTextureLoader().load(path)
            atlas_size = glm.vec2(atlas.size.xy)

            x = obj.x
            y = self.context.size.y - obj.y - obj.height
            lower_left = glm.vec2(x, y)
            logger.debug(f"lower_left: {lower_left}")

            width = obj.width
            height = obj.height

            size = glm.vec2(width, height)

            # Calculate half dimensions for centering
            center = size / 2.0

            logger.debug(f"center: {center}")
            
            # Handle rotation in radians
            rotation = -glm.radians(obj.rotation)
            logger.debug(f"rotation: {rotation}")

            rotated_offset = glm.rotate(center, rotation)
            logger.debug(f"rotated_offset: {rotated_offset}")

            position = lower_left + rotated_offset
            position.y = position.y + self.context.map.tileheight
            logger.debug(f"position: {position}")

            # Calculate scale
            scale = glm.vec2(width / atlas_size.x, height / atlas_size.y)
            sampler = DefaultSpriteSampler()

            # Build the sprite
            sprite_builder = CollidableSpriteBuilder()
            color = glm.vec4(1.0, 1.0, 1.0, self.context.opacity)
            sprite = sprite_builder.build(
                #atlas, Rect2i(0, 0, width, height), sampler=sampler, color=color
                atlas, Rect2i(0, 0, atlas_size.x, atlas_size.y), sampler=sampler, color=color
            )

            logger.debug(f"sprite: {sprite}")

            if self.create_node_cb is not None:
                node = self.create_node_cb(position, rotation, scale, sprite, properties)
            else:
                node = self.create_node(position, rotation, scale, sprite, properties)

            # Attach the node to the appropriate layer
            if node is not None:
                self.context.layer.attach(node)

    def create_node(self, position: glm.vec2, rotation: float, scale: glm.vec2, sprite: Sprite, properties: dict):
        node = Node2D(position, rotation, scale, vu=SpriteVu(), model=sprite)
        return node
