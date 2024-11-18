from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.loader.xml_sprite_atlas_loader import XmlSpriteAtlasLoader
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

from ..demo import Demo

from .thing import Thing
from .floor import Floor

class ThingsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.draw_options: DrawOptions = None
        #self.reset()

    def _create(self):
        super()._create()
        self.draw_options = DrawOptions(self.view.scratch)
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine(draw_options=self.draw_options)
        self.physics_engine.create()
        self.create_floor()

        atlas = self.atlas  = XmlSpriteAtlasLoader().load(":resources:/platformer/Spritesheets/spritesheet_tiles.xml")
        logger.debug(f"atlas: {atlas}")

        self.sprite = atlas.get("bomb.png")


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
            self.create_thing(glm.vec2(x, y))


    def create_thing(self, position):
        thing = Thing(position, self.sprite)
        thing.create()
        self.scene.attach(thing)

    def create_floor(self):
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(self.width, 20))
        floor.create()
        self.scene.attach(floor)


    def draw(self, renderer: Renderer):
        self.physics_engine.debug_draw(renderer)
        imgui.begin("Shapes")
        imgui.text("Click to create shapes")

        if imgui.button("Reset"):
            self.reset()

        if imgui.begin_list_box("##Sprites", (-1, -1)):

            for name, sprite in self.atlas.sprite_map.items():
                opened, selected = imgui.selectable(name, sprite == self.sprite)
                if opened:
                    logger.debug(f"Selected: {name}")
                    self.sprite = sprite

            imgui.end_list_box()
        
        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.scene.update(delta_time)
        self.physics_engine.update(1/60)

def main():
    ThingsDemo().create().run()


if __name__ == "__main__":
    main()
