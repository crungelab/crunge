from loguru import logger
import glm
from pytmx import TiledObject

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.sprite.sprite_sampler import DefaultSpriteSampler, RepeatingSpriteSampler
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
            pass

        elif obj.image:
            x = obj.x
            y = self.context.size.y - obj.y
            lower_left = glm.vec2(x, y)
            width = obj.width
            height = obj.height
            #lower_left = glm.vec2(x, y)

            size = glm.vec2(width, height)

            # Calculate half dimensions for centering
            #center = size / 2.0
            center = glm.vec2(width // 2, height // 2)
            center.y = -center.y
            logger.debug(f"center: {center}")
            
            # Handle rotation in radians
            rotation = -glm.radians(obj.rotation)

            rotated_offset = glm.rotate(center, rotation)
            position = lower_left + rotated_offset

            # Load the texture atlas
            image = obj.image
            path = image[0]
            atlas = ImageTextureLoader().load(path)
            atlas_size = glm.vec2(atlas.size.xy)

            # Choose sampler based on atlas size
            #sampler = DefaultSpriteSampler() if size <= atlas_size else RepeatingSpriteSampler()
            sampler = DefaultSpriteSampler()

            # Build the sprite
            sprite_builder = CollidableSpriteBuilder()
            color = glm.vec4(1.0, 1.0, 1.0, self.context.opacity)
            sprite = sprite_builder.build(
                atlas, Rect2i(0, 0, width, height), sampler=sampler, color=color
            )

            logger.debug(f"sprite: {sprite}")

            if self.create_node_cb is not None:
                node = self.create_node_cb(position, rotation, sprite, properties)
            else:
                node = self.create_node(position, rotation, sprite, properties)

            # Attach the node to the appropriate layer
            if node is not None:
                self.context.layer.attach(node)

    def create_node(self, position: glm.vec2, rotation: float, sprite: Sprite, properties: dict):
        size = glm.vec2(sprite.width, sprite.height)
        node = Node2D(position, size=size, vu=SpriteVu(), model=sprite)
        node.rotation = rotation
        return node
