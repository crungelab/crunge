from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...physics import DynamicPhysicsEngine

from .ball import Ball
from .floor import Floor

class BallsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine()
        self.physics_engine.create()
        self.create_floor()

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

    def create_floor(self):
        x = self.width / 2
        y = -10
        position = glm.vec2(x, y)
        floor = Floor(position, glm.vec2(self.width, 20))
        floor.create()
        self.scene.attach(floor)

    def draw(self, renderer: Renderer):
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
    BallsDemo().create().run()


if __name__ == "__main__":
    main()