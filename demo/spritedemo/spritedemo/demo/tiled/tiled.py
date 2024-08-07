from pathlib import Path

from loguru import logger
import glm
from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...sprite import Sprite
from ...node_2d import Node2D
from ...texture_kit import TextureKit
from ...texture_atlas_kit import TextureAtlasKit
from ...texture import Texture


class TiledDemo(Demo):
    def __init__(self):
        super().__init__()

        tmx_path = self.resource_root / "tiled" / "level1.tmx"
        self.tmx_data = TiledMap(tmx_path)
        self.reset()

    def reset(self):
        self.scene.clear()
        self.create_map()


    def create_view(self):
        super().create_view()
        self.camera.zoom = .5

    def create_map(self):

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
                    atlas = TextureKit().load(path)
                    logger.debug(f"atlas: {atlas}")

                    rect = image[1]
                    if rect:
                        tx, ty, tw, th = rect
                        texture = Texture(atlas.texture, int(tx), int(ty), int(tw), int(th), atlas)
                        logger.debug(f"texture: {texture}")
                    else:
                        texture = atlas

                    sprite = Sprite(texture)
                    node = Node2D(glm.vec2(x ,y), vu=sprite)
                    self.scene.add_child(node)

            elif isinstance(layer, TiledObjectGroup):
                # iterate over all the objects in the layer
                for obj in layer:
                    logger.debug(obj)

                    # objects with points are polygons or lines
                    if hasattr(obj, "points"):
                        #draw_lines(poly_color, obj.closed, obj.points, 3)
                        pass

                    # some object have an image
                    elif obj.image:
                        logger.debug(f"obj.image: {obj.image}")

                        image = obj.image
                        x = obj.x
                        #y = mh - obj.y
                        y = pixel_height - obj.y
                        path = image[0]
                        atlas = TextureKit().load(path)
                        logger.debug(f"atlas: {atlas}")

                        rect = image[1]
                        if rect:
                            tx, ty, tw, th = rect
                            texture = Texture(atlas.texture, int(tx), int(ty), int(tw), int(th), atlas)
                            logger.debug(f"texture: {texture}")
                        else:
                            texture = atlas

                        sprite = Sprite(texture)
                        node = Node2D(glm.vec2(x ,y), vu=sprite)
                        self.scene.add_child(node)

                    # draw a rect for everything else
                    else:
                        #draw_rect(rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                        pass


    def draw(self, renderer: Renderer):
        # imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Tiled")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

def main():
    TiledDemo().create().run()


if __name__ == "__main__":
    main()
