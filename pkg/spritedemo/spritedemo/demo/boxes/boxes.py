from pathlib import Path

from loguru import logger
import glm
import pymunk

from crunge import sdl, imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...sprite import Sprite
from ...node_2d import Node2D
from ...texture_kit import TextureKit

from .box import Box
from ...physics import DynamicPhysicsEngine
class BoxesDemo(Demo):
    def __init__(self):
        super().__init__()
        self.last_mouse = glm.vec2(0, 0)
        # Our physics engine
        self.physics_engine = physics_engine = DynamicPhysicsEngine()
        self.space = physics_engine.space
        self.physics_engine.setup()

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
            self.create_box(glm.vec2(x, y))


    def create_box(self, position):
        box = Box(position)
        box.setup()
        self.scene.add_child(box)

    def reset(self):
        pass

    def draw(self, renderer: Renderer):
        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.scene.update(delta_time)
        self.physics_engine.update(1/60)

def main():
    BoxesDemo().create().run()


if __name__ == "__main__":
    main()
