from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.d2.physics import DynamicPhysicsEngine

from ..demo import Demo

from .box import Box
from .floor import Floor


class BoxesDemo(Demo):
    def reset(self):
        super().reset()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine().create()
        self.create_floor()

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

            logger.debug(f"Creating box at {x}, {y}")
            self.create_box(world_vec)

    def create_box(self, position):
        self.scene.attach(Box(position))

    def create_floor(self):
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(self.width, 20))
        floor.create()
        self.scene.attach(floor)

    def _draw(self):
        imgui.begin("Boxes Demo")
        imgui.text("Click to create boxes")

        self.draw_stats()

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super()._draw()

    def update(self, delta_time: float):
        self.physics_engine.update(1 / 60)
        self.scene.update(delta_time)
        super().update(delta_time)


def main():
    BoxesDemo().run()


if __name__ == "__main__":
    main()
