from loguru import logger
import glm
from pytmx import TiledObject

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.sprite.sprite_sampler import DefaultSpriteSampler, RepeatingSpriteSampler
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from .object_builder import ObjectBuilder


class DefaultObjectBuilder(ObjectBuilder):
    def build(self, obj: TiledObject, properties: dict):
        # Check if the object is a polygon or line
        if hasattr(obj, "points"):
            # Handle polygons or lines if needed
            pass

        elif obj.image:
            x = obj.x
            y = obj.y
            #lower_left = glm.vec2(x, y)

            width, height = obj.width, obj.height
            size = glm.ivec2(width, height)

            # Calculate half dimensions for centering
            half_width = width / 2
            half_height = height / 2

            center_x = half_width
            center_y = half_height
            
            # Handle rotation in radians
            rotation = -glm.radians(obj.rotation)

            cos_rotation = glm.cos(rotation)
            sin_rotation = glm.sin(rotation)
            rotated_center_x = center_x * cos_rotation - center_y * sin_rotation
            rotated_center_y = center_x * sin_rotation + center_y * cos_rotation
            #position = glm.vec2(x + rotated_center_x, y - rotated_center_y)
            position = glm.vec2(x + rotated_center_x, self.context.size - (y + rotated_center_y))
            #position = glm.vec2(x, y)

            # Load the texture atlas
            image = obj.image
            path = image[0]
            atlas = ImageTextureLoader().load(path)

            # Choose sampler based on atlas size
            sampler = DefaultSpriteSampler() if size <= glm.ivec2(atlas.size) else RepeatingSpriteSampler()

            # Build the sprite
            sprite_builder = CollidableSpriteBuilder()
            color = glm.vec4(1.0, 1.0, 1.0, self.context.opacity)
            sprite = sprite_builder.build(
                atlas, Rect2i(0, 0, width, height), sampler=sampler, color=color
            )

            logger.debug(f"sprite: {sprite}")

            # Create a SpriteVu (visual unit)
            vu = SpriteVu(sprite).create()

            # Create a Node2D to represent the sprite in the scene
            #node = Node2D(position, size=size, vu=vu)
            node = Node2D(position, vu=vu, model=sprite)
            node.rotation = rotation

            # Attach the node to the appropriate layer
            self.context.layer.attach(node)
