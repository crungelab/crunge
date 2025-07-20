from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

from ..demo import Demo

from .thing import Thing
from .floor import Floor


class ThingsDemo(Demo):
    def reset(self):
        super().reset()
        self.debug_draw_enabled = False
        self.draw_options = DrawOptions(self.view.scratch)

        #self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine()
        self.physics_engine.create()
        self.create_floor()

        atlas = self.atlas = XmlSpriteAtlasLoader(sprite_builder=CollidableSpriteBuilder()).load(
            ":resources:/platformer/Spritesheets/spritesheet_tiles.xml"
        )
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
            mouse_vec = glm.vec2(event.x, event.y)
            world_vec = self.camera.unproject(mouse_vec)
            x, y = world_vec.x, world_vec.y
            logger.debug(f"Creating thing at {x}, {y}")
            self.create_thing(world_vec)

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
        imgui.begin("Shapes")
        imgui.text("Click to create shapes")

        _, self.debug_draw_enabled = imgui.checkbox("Debug Draw", self.debug_draw_enabled)

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

        if self.debug_draw_enabled:
            self.physics_engine.debug_draw(self.draw_options)

        super().draw(renderer)

    def update(self, delta_time: float):
        self.physics_engine.update(1 / 60)
        super().update(delta_time)


def main():
    ThingsDemo().run()


if __name__ == "__main__":
    main()
