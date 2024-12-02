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
            y = self.context.pixel_height - obj.y
            width = obj.width
            height = obj.height
            #lower_left = glm.vec2(x, y)

            size = glm.vec2(width, height)

            # Calculate half dimensions for centering
            center = size / 2.0
            center.y = -center.y
            logger.debug(f"center: {center}")
            
            # Handle rotation in radians
            rotation = -glm.radians(obj.rotation)

            cos_rotation = glm.cos(rotation)
            sin_rotation = glm.sin(rotation)
            rotated_center_x = (center.x * cos_rotation) - (center.y * sin_rotation)
            rotated_center_y = (center.x * sin_rotation) + (center.y * cos_rotation)
            position = glm.vec2(x + rotated_center_x, y + rotated_center_y)
            #position = glm.vec2(x + rotated_center_x, self.context.pixel_height - (y + rotated_center_y))
            #position = glm.vec2(x, self.context.pixel_height - y)
            #position = glm.vec2(x, y) + center
            #position = glm.vec2(x + center.x, y + center.y)

            # Load the texture atlas
            image = obj.image
            path = image[0]
            atlas = ImageTextureLoader().load(path)
            atlas_size = glm.vec2(atlas.size.xy)

            # Choose sampler based on atlas size
            sampler = DefaultSpriteSampler() if size <= atlas_size else RepeatingSpriteSampler()

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

            '''
            # Create a SpriteVu (visual unit)
            vu = SpriteVu(sprite).create()

            # Create a Node2D to represent the sprite in the scene
            #node = Node2D(position, size=size, vu=vu)
            node = Node2D(position, vu=vu, model=sprite)
            node.rotation = rotation
            '''

            # Attach the node to the appropriate layer
            if node is not None:
                self.context.layer.attach(node)

    def create_node(self, position: glm.vec2, rotation: float, sprite: Sprite, properties: dict):
        vu = SpriteVu(sprite).create()
        size = glm.vec2(sprite.width, sprite.height)
        node = Node2D(position, size=size, vu=vu, model=sprite)
        node.rotation = rotation
        return node
