from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.loader.texture_atlas_loader import TextureAtlasLoader

from ..demo import Demo
from ...physics import DynamicPhysicsEngine

from .thing import Thing
from .floor import Floor

class ThingsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2(0, 0)
        self.physics_engine = DynamicPhysicsEngine()
        self.physics_engine.create()
        self.create_floor()

        atlas = self.atlas  = TextureAtlasLoader().load(":resources:/platformer/Spritesheets/spritesheet_tiles.xml")
        logger.debug(f"atlas: {atlas}")

        self.texture = atlas.get("bomb.png")


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
            self.create_box(glm.vec2(x, y))


    def create_box(self, position):
        box = Thing(position, self.texture)
        box.create()
        self.scene.root.attach(box)

    def create_floor(self):
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        box = Floor(position, glm.vec2(self.width, 20))
        box.create()
        self.scene.root.attach(box)


    def draw(self, renderer: Renderer):
        imgui.begin("Shapes")
        imgui.text("Click to create shapes")

        if imgui.button("Reset"):
            self.reset()

        if imgui.begin_list_box("Textures", (-1, -1)):

            for name, texture in self.atlas.textures.items():
                opened, selected = imgui.selectable(name, texture == self.texture)
                if opened:
                    logger.debug(f"Selected: {name}")
                    self.texture = texture
                    #self.sprite.texture = texture

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
