from pathlib import Path

from loguru import logger
import glm
from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge import imgui
from crunge.engine import Renderer

from crunge.engine import RectI
from crunge.engine.d2.sprite import Sprite
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture_loader import TextureLoader
from crunge.engine.resource.texture import Texture

from ..demo import Demo


class TiledDemo(Demo):
    def __init__(self):
        super().__init__()

        #tmx_path = self.resource_root / "tiled" / "level1.tmx"
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        self.tmx_data = TiledMap(tmx_path)
        self.reset()

    def reset(self):
        self.scene.clear()
        self.create_map()

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2

    def create_map(self):

        name = self.tmx_data.filename
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        mw = self.tmx_data.width
        mh = self.tmx_data.height - 1
        pixel_height = mh * th

        for i, layer in enumerate(self.tmx_data.visible_layers):
            if isinstance(layer, TiledTileLayer):
                # iterate over the tiles in the layer
                for x, y, image in layer.tiles():
                    y = mh - y
                    x = x * tw
                    y = y * th
                    logger.debug(f"Tile: {x}, {y}, {image}")

                    path = image[0]
                    atlas = TextureLoader().load(path)
                    logger.debug(f"atlas: {atlas}")

                    rect = image[1]
                    if rect:
                        tx, ty, tw, th = rect
                        texture = Texture(
                            atlas.texture,
                            RectI(tx, ty, tw, th),
                            atlas,
                        ).set_name(name)
                        logger.debug(f"texture: {texture}")
                    else:
                        texture = atlas

                    sprite = Sprite(texture)
                    node = Node2D(glm.vec2(x, y), vu=sprite)
                    self.scene.root.attach(node)

            elif isinstance(layer, TiledObjectGroup):
                for obj in layer:
                    logger.debug(obj)

                    # objects with points are polygons or lines
                    if hasattr(obj, "points"):
                        pass

                    elif obj.image:
                        logger.debug(f"obj.image: {obj.image}")

                        image = obj.image
                        x = obj.x
                        y = pixel_height - obj.y
                        path = image[0]
                        atlas = TextureLoader().load(path)
                        logger.debug(f"atlas: {atlas}")

                        rect = image[1]
                        if rect:
                            tx, ty, tw, th = rect
                            texture = Texture(
                                atlas.texture,
                                RectI(tx, ty, tw, th),
                                atlas,
                            ).set_name(name)
                            logger.debug(f"texture: {texture}")
                        else:
                            texture = atlas

                        sprite = Sprite(texture)
                        node = Node2D(glm.vec2(x, y), vu=sprite)
                        self.scene.root.attach(node)

                    # draw a rect for everything else
                    else:
                        # draw_rect(rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                        pass

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Tiled")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)


def main():
    TiledDemo().create().run()


if __name__ == "__main__":
    main()
