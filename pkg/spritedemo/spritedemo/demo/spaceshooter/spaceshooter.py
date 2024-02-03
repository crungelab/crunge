from pathlib import Path

from loguru import logger
import glm

from crunge import sdl, imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...sprite import Sprite
from ...node_2d import Node2D
from ...texture_atlas_kit import TextureAtlasKit
from ...physics import DynamicPhysicsEngine
from .ship import Ship

class SpaceShooter(Demo):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

        self.physics_engine = DynamicPhysicsEngine(gravity=(0, 0))
        self.physics_engine.create()

        self.create_ship(glm.vec2(self.width / 2, self.height / 2))

    def create_ship(self, position):
        ship = self.ship = Ship(position)
        self.node = ship
        ship.create()
        self.scene.add_child(ship)

    def reset(self):
        self.scale = 1.0
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

    def draw(self, renderer: Renderer):
        # imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Ship")

        # Rotation
        '''
        changed, self.angle = imgui.drag_float(
            "Angle",
            self.angle,
        )
        self.node.angle = self.angle
        '''
        
        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        self.node.scale = glm.vec2(self.scale, self.scale)

        #TODO: Implement alpha and color
        '''
        # Alpha
        changed, self.alpha = imgui.drag_int("Alpha", self.alpha, 1, 0, 255)
        self.sprite.alpha = self.alpha

        # Color
        _, self.color_enabled = imgui.checkbox("Tint", self.color_enabled)
        if self.color_enabled:
            changed, self.color = imgui.color_edit3("Color", *self.color)
            self.sprite.color = (
                int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255),
            )
        else:
            self.sprite.color = 255, 255, 255
        '''

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        #self.scene.update(delta_time)
        self.physics_engine.update(1/60)
        self.scene.update(delta_time)

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.keysym.sym
        state = event.state
        if key == sdl.SDLK_s:
            if state == 1:
                self.ship.front_thruster.on()
            else:
                self.ship.front_thruster.off()
        if key == sdl.SDLK_w:
            if state == 1:
                self.ship.rear_thruster.on()
            else:
                self.ship.rear_thruster.off()
        elif key == sdl.SDLK_a:
            if state == 1:
                self.ship.left_thruster.on()
            else:
                self.ship.left_thruster.off()
        elif key == sdl.SDLK_d:
            if state == 1:
                self.ship.right_thruster.on()
            else:
                self.ship.right_thruster.off()

def main():
    SpaceShooter().create().run()


if __name__ == "__main__":
    main()
