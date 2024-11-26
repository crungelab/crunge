from loguru import logger
import glm

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from .object_builder import ObjectBuilder

class DefaultObjectBuilder(ObjectBuilder):
    def build(self, obj, properties):
        #logger.debug(obj)

        # objects with points are polygons or lines
        if hasattr(obj, "points"):
            pass

        elif obj.image:
            #logger.debug(f"obj.image: {obj.image}")

            image = obj.image
            x = obj.x
            y = self.context.pixel_height - obj.y
            path = image[0]
            atlas = ImageTextureLoader().load(path)
            #logger.debug(f"atlas: {atlas}")

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
            size=glm.vec2(obj.width, obj.height)
            logger.debug(f"size: {size}")
            node = Node2D(glm.vec2(x, y), size=size, vu=vu)
            #self.context.scene.attach(node)
            self.context.layer.attach(node)

