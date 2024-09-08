from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...physics import DynamicPhysicsEngine

from .box import Box
from .floor import Floor

class BoxesDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2(0, 0)
        self.physics_engine = DynamicPhysicsEngine()
        self.physics_engine.create()
        self.create_floor()

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        x, y = event.x, event.y
        self.last_mouse = glm.vec2(x, y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        button = event.button
        action = event.state == 1
        if button == 1 and action:
            x = self.last_mouse.x
            y = self.height - self.last_mouse.y
            logger.debug(f"Creating box at {x}, {y}")
            self.create_box(glm.vec2(x, y))


    def create_box(self, position):
        box = Box(position)
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
        imgui.begin("Boxes Demo")
        imgui.text("Click to create boxes")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.scene.update(delta_time)
        self.physics_engine.update(1/60)

def main():
    BoxesDemo().create().run()


if __name__ == "__main__":
    main()
