from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder

from ..physics_demo import PhysicsDemo

from .thing import Thing
from .floor import Floor


class ThingsDemo(PhysicsDemo):
    def reset(self):
        super().reset()
        self.last_mouse = glm.vec2()
        self.create_floor()

        atlas = self.atlas = XmlSpriteAtlasLoader(
            sprite_builder=CollidableSpriteBuilder()
        ).load(":resources:/platformer/Spritesheets/spritesheet_tiles.xml")
        logger.debug(f"atlas: {atlas}")

        self.sprite = atlas.get("bomb.png")

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)  # right-click drag handled here
        if event.button == 1 and event.down:
            world = self.camera.unproject(glm.vec2(event.x, event.y))
            logger.debug(f"Creating box at {world}")
            self.create_thing(world)

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

    def _draw(self):
        imgui.begin("Shapes")
        imgui.text("Click to create shapes")

        self.draw_stats()
        self.draw_physics_options()

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

        super()._draw()

    def update(self, delta_time: float):
        self.world.update(1 / 60)
        super().update(delta_time)


def main():
    ThingsDemo().run()


if __name__ == "__main__":
    main()
