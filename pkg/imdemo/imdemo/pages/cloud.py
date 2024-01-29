from crunge import engine
from ludi import Point, Vector
from ludi.utils import _Vec2  # bring in "private" class
import os
import random
import pyglet

from crunge import imgui

from imdemo.page import Page
from imdemo.particle import AnimatedAlphaParticle

SCREEN_TITLE = "Particle based fireworks"

CLOUD_TEXTURES = [
    ludi.make_soft_circle_texture(50, ludi.color.WHITE),
    ludi.make_soft_circle_texture(50, ludi.color.LIGHT_GRAY),
    ludi.make_soft_circle_texture(50, ludi.color.LIGHT_BLUE),
]

class CloudPage(Page):
    def reset(self):
        self.create_emitter()
        self.fullwidth=self.fullheight=False

    def on_show(self):
        ludi.set_background_color(ludi.color.BLACK)

    def create_emitter(self):
        self.emitter = ludi.Emitter(
            center_xy=(64, self.window.height/2),
            change_xy=(0.15, 0),
            emit_controller=ludi.EmitMaintainCount(60),
            particle_factory=lambda emitter: AnimatedAlphaParticle(
                filename_or_texture=random.choice(CLOUD_TEXTURES),
                change_xy=(_Vec2(ludi.rand_in_circle((0.0, 0.0), 0.04)) + _Vec2(0.1, 0)).as_tuple(),
                start_alpha=0,
                duration1=random.uniform(5.0, 10.0),
                mid_alpha=255,
                duration2=random.uniform(5.0, 10.0),
                end_alpha=0,
                center_xy=ludi.rand_in_circle((0.0, 0.0), 50)
            )
        )

    def update(self, delta_time):
        if self.emitter.center_x > self.window.width:
            self.emitter.center_x = 0
        self.emitter.update()

    def draw(self):
        #gui.set_next_window_pos((self.window.width - 288, 32), imgui.COND_ONCE)
        #gui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Cloud")
        if imgui.button("Reset"):
            self.reset()
        imgui.end()

        self.emitter.draw()

    def on_key_press(self, key, modifiers):
        if key == ludi.key.ESCAPE:
            ludi.close_window()

def install(app):
    app.add_page(CloudPage, "cloud", "Cloud")
