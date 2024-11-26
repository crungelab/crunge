from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder.builder_context import SceneBuilderContext
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

from ..demo import Demo

from .ball import Ball
from .tile import Tile

class TiledPhysicsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.debug_draw_enabled = False

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
            logger.debug(f"Creating ball at {x}, {y}")
            self.create_ball(glm.vec2(x, y))


    def create_ball(self, position):
        ball = Ball(position)
        ball.create()
        self.scene.attach(ball)

    def create_map(self):
        context = SceneBuilderContext(scene=self.scene)
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader = TiledMapLoader(context, map_builder=DefaultMapBuilder(context))
        map_loader.load(tmx_path)

    '''
    def create_map(self):

        name = self.map.filename
        tw = self.map.tilewidth
        th = self.map.tileheight
        mw = self.map.width
        mh = self.map.height - 1
        pixel_height = mh * th

        sprite_builder=CollidableSpriteBuilder()


        #for layer in self.map.visible_layers:
        for layer in self.map.layers:
            if isinstance(layer, TiledTileLayer):
                logger.debug(f"Layer: {layer}")
                logger.debug(f"Layer properties: {layer.properties}")
                layer_class = layer.properties.get("class", None)  # Access the 'class' property
                if layer_class:
                    print(f"Layer '{layer.name}' has class: {layer_class}")
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
                        sprite = sprite_builder.build(atlas, Rect2i(tx, ty, tw, th))
                    else:
                        sprite = sprite_builder.build(atlas, Rect2i(0, 0, atlas.width, atlas.height))

                    node = Tile(glm.vec2(x, y), sprite)
                    self.scene.attach(node)

            elif isinstance(layer, TiledObjectGroup):
                pass
                    # draw a rect for everything else
            else:
                # draw_rect(rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                pass
    '''

    def draw(self, renderer: Renderer):        
        imgui.begin("Tiled Physics Demo")

        imgui.text("Click to create balls")

        _, self.debug_draw_enabled = imgui.checkbox("Debug Draw", self.debug_draw_enabled)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        if self.debug_draw_enabled:
            self.physics_engine.debug_draw(renderer)

        super().draw(renderer)

    def update(self, delta_time: float):
        self.physics_engine.update(1/60)
        super().update(delta_time)

def main():
    TiledPhysicsDemo().create().run()


if __name__ == "__main__":
    main()
