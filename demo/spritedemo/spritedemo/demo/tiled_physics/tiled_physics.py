from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge.engine.math import Rect2i
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader
from crunge.engine.resource.texture import Texture
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from ..demo import Demo

from .ball import Ball
from .tile import Tile


class TiledPhysicsDemo(Demo):
    def __init__(self):
        super().__init__()
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        self.map = TiledMap(tmx_path)

    def _create(self):
        super()._create()
        self.draw_options = DrawOptions(self.view.scratch)
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine(draw_options=self.draw_options).create()
        self.create_map()

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        x, y = event.x, event.y
        self.last_mouse = glm.vec2(x, y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        button = event.button
        down = event.down
        if button == 1 and down:
            x = self.last_mouse.x
            y = self.height - self.last_mouse.y
            logger.debug(f"Creating box at {x}, {y}")
            self.create_ball(glm.vec2(x, y))


    def create_ball(self, position):
        ball = Ball(position)
        ball.create()
        self.scene.attach(ball)

    def create_map(self):

        name = self.map.filename
        tw = self.map.tilewidth
        th = self.map.tileheight
        mw = self.map.width
        mh = self.map.height - 1
        pixel_height = mh * th

        sprite_builder=CollidableSpriteBuilder()

        for i, layer in enumerate(self.map.visible_layers):
            if isinstance(layer, TiledTileLayer):
                # iterate over the tiles in the layer
                for x, y, image in layer.tiles():
                    y = mh - y
                    x = x * tw
                    y = y * th
                    #logger.debug(f"Tile: {x}, {y}, {image}")

                    path = image[0]
                    atlas = ImageTextureLoader().load(path)
                    #logger.debug(f"atlas: {atlas}")

                    rect = image[1]
                    if rect:
                        tx, ty, tw, th = rect
                        '''
                        sprite = Sprite(
                            atlas,
                            Rect2i(tx, ty, tw, th),
                        ).set_name(name)
                        '''
                        sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
                        #logger.debug(f"texture: {texture}")
                    else:
                        #texture = atlas
                        sprite = Sprite(atlas).set_name(name)

                    #sprite = Sprite(texture)

                    #node = Node2D(glm.vec2(x, y), vu=vu)
                    node = Tile(glm.vec2(x, y), sprite)
                    self.scene.attach(node)

            elif isinstance(layer, TiledObjectGroup):
                pass
                    # draw a rect for everything else
            else:
                # draw_rect(rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                pass

    def draw(self, renderer: Renderer):
        self.physics_engine.debug_draw(renderer)
        
        imgui.begin("Balls Demo")
        imgui.text("Click to create balls")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.scene.update(delta_time)
        self.physics_engine.update(1/60)

def main():
    TiledPhysicsDemo().create().run()


if __name__ == "__main__":
    main()