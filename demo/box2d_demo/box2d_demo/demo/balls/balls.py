from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from ..physics_demo import PhysicsDemo

from .ball import Ball
from .floor import Floor


class BallsDemo(PhysicsDemo):
    def reset(self):
        super().reset()
        self.last_mouse = glm.vec2()
        self.create_floor()

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)  # right-click drag handled here
        if event.button == 1 and event.down:
            world = self.camera.unproject(glm.vec2(event.x, event.y))
            logger.debug(f"Creating box at {world}")
            self.create_ball(world)

    def create_ball(self, position):
        self.scene.attach(Ball(position))

    def create_floor(self):
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(self.width, 20))
        self.scene.attach(floor)

    def _draw(self):
        imgui.begin("Balls Demo")
        imgui.text("Click to create balls")

        self.draw_stats()
        self.draw_physics_options()

        if imgui.button("Reset"):
            self.reset()

        imgui.end()
        super()._draw()

    """
    def update(self, delta_time: float):
        with self.physics_engine.update(1 / 60):
            self.scene.update(delta_time)
            super().update(delta_time)
    """

    def update(self, delta_time: float):
        self.world.update(1 / 60)
        self.scene.update(delta_time)
        super().update(delta_time)

def main():
    BallsDemo().run()


if __name__ == "__main__":
    main()
