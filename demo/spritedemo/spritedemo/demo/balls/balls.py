from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.d2.physics import DynamicPhysicsEngine

from ..demo import Demo

from .ball import Ball
from .floor import Floor

class BallsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine().create()
        #self.physics_engine.create()
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
            logger.debug(f"Creating ball at {x}, {y}")
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
        self.physics_engine.update(1/60)
        self.scene.update(delta_time)
        super().update(delta_time)

def main():
    BallsDemo().create().run()


if __name__ == "__main__":
    main()
