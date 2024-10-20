from crunge import shell
from ludi import Point, Vector
from ludi.utils import _Vec2  # bring in "private" class
import os
import random
import pyglet

from crunge import imgui

from imdemo.page import Page

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Particle based fireworks"
LAUNCH_INTERVAL_MIN = 1.5
LAUNCH_INTERVAL_MAX = 2.5
TEXTURE = "images/pool_cue_ball.png"
RAINBOW_COLORS = (
    ludi.color.ELECTRIC_CRIMSON,
    ludi.color.FLUORESCENT_ORANGE,
    ludi.color.ELECTRIC_YELLOW,
    ludi.color.ELECTRIC_GREEN,
    ludi.color.ELECTRIC_CYAN,
    ludi.color.MEDIUM_ELECTRIC_BLUE,
    ludi.color.ELECTRIC_INDIGO,
    ludi.color.ELECTRIC_PURPLE,
)
SPARK_TEXTURES = [ludi.make_circle_texture(8, clr) for clr in RAINBOW_COLORS]
SPARK_PAIRS = [
    [SPARK_TEXTURES[0], SPARK_TEXTURES[3]],
    [SPARK_TEXTURES[1], SPARK_TEXTURES[5]],
    [SPARK_TEXTURES[7], SPARK_TEXTURES[2]],
]
ROCKET_SMOKE_TEXTURE = ludi.make_soft_circle_texture(15, ludi.color.GRAY)
PUFF_TEXTURE = ludi.make_soft_circle_texture(80, (40, 40, 40))
FLASH_TEXTURE = ludi.make_soft_circle_texture(70, (128, 128, 90))
CLOUD_TEXTURES = [
    ludi.make_soft_circle_texture(50, ludi.color.WHITE),
    ludi.make_soft_circle_texture(50, ludi.color.LIGHT_GRAY),
    ludi.make_soft_circle_texture(50, ludi.color.LIGHT_BLUE),
]
STAR_TEXTURES = [
    ludi.make_soft_circle_texture(8, ludi.color.WHITE),
    ludi.make_soft_circle_texture(8, ludi.color.PASTEL_YELLOW),
]
SPINNER_HEIGHT = 75


def make_spinner():
    spinner = ludi.Emitter(
        center_xy=(SCREEN_WIDTH / 2, SPINNER_HEIGHT - 5),
        emit_controller=ludi.EmitterIntervalWithTime(0.025, 2.0),
        particle_factory=lambda emitter: ludi.FadeParticle(
            filename_or_texture=random.choice(STAR_TEXTURES),
            change_xy=(0, 6.0),
            lifetime=0.2
        )
    )
    spinner.change_angle = 16.28
    return spinner


def make_rocket(emit_done_cb):
    """Emitter that displays the smoke trail as the firework shell climbs into the sky"""
    rocket = RocketEmitter(
        center_xy=(random.uniform(100, SCREEN_WIDTH - 100), 25),
        emit_controller=ludi.EmitterIntervalWithTime(0.04, 2.0),
        particle_factory=lambda emitter: ludi.FadeParticle(
            filename_or_texture=ROCKET_SMOKE_TEXTURE,
            change_xy=ludi.rand_in_circle((0.0, 0.0), 0.08),
            scale=0.5,
            lifetime=random.uniform(1.0, 1.5),
            start_alpha=100,
            end_alpha=0,
            mutation_callback=rocket_smoke_mutator
        ),
        emit_done_cb=emit_done_cb
    )
    rocket.change_x = random.uniform(-1.0, 1.0)
    rocket.change_y = random.uniform(5.0, 7.25)
    return rocket


def make_flash(prev_emitter):
    """Return emitter that displays the brief flash when a firework shell explodes"""
    return ludi.Emitter(
        center_xy=prev_emitter.get_pos(),
        emit_controller=ludi.EmitBurst(3),
        particle_factory=lambda emitter: ludi.FadeParticle(
            filename_or_texture=FLASH_TEXTURE,
            change_xy=ludi.rand_in_circle((0.0, 0.0), 3.5),
            lifetime=0.15
        )
    )


def make_puff(prev_emitter):
    """Return emitter that generates the subtle smoke cloud left after a firework shell explodes"""
    return ludi.Emitter(
        center_xy=prev_emitter.get_pos(),
        emit_controller=ludi.EmitBurst(4),
        particle_factory=lambda emitter: ludi.FadeParticle(
            filename_or_texture=PUFF_TEXTURE,
            change_xy=(_Vec2(ludi.rand_in_circle((0.0, 0.0), 0.4)) + _Vec2(0.3, 0.0)).as_tuple(),
            lifetime=4.0
        )
    )

def clamp(a, low, high):
    if a > high:
        return high
    elif a < low:
        return low
    else:
        return a

class AnimatedAlphaParticle(ludi.LifetimeParticle):
    """A custom particle that animates between three different alpha levels"""

    def __init__(
            self,
            filename_or_texture: ludi.FilenameOrTexture,
            change_xy: Vector,
            start_alpha: int = 0,
            duration1: float = 1.0,
            mid_alpha: int = 255,
            duration2: float = 1.0,
            end_alpha: int = 0,
            center_xy: Point = (0.0, 0.0),
            angle: float = 0,
            change_angle: float = 0,
            scale: float = 1.0,
            mutation_callback=None,
    ):
        super().__init__(filename_or_texture, change_xy, duration1 + duration2, center_xy, angle, change_angle, scale,
                         start_alpha, mutation_callback)
        self.start_alpha = start_alpha
        self.in_duration = duration1
        self.mid_alpha = mid_alpha
        self.out_duration = duration2
        self.end_alpha = end_alpha

    def update(self):
        super().update()
        if self.lifetime_elapsed <= self.in_duration:
            u = self.lifetime_elapsed / self.in_duration
            self.alpha = clamp(ludi.lerp(self.start_alpha, self.mid_alpha, u), 0, 255)
        else:
            u = (self.lifetime_elapsed - self.in_duration) / self.out_duration
            self.alpha = clamp(ludi.lerp(self.mid_alpha, self.end_alpha, u), 0, 255)


class RocketEmitter(ludi.Emitter):
    """Custom emitter class to add gravity to the emitter to represent gravity on the firework shell"""

    def update(self):
        super().update()
        # gravity
        self.change_y += -0.05

class FireworksPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        #file_path = os.path.dirname(os.path.abspath(__file__))
        #os.chdir(file_path)

        ludi.set_background_color(ludi.color.BLACK)
        self.emitters = []

        self.launch_firework(0)
        ludi.schedule(self.launch_spinner, 4.0)

        stars = ludi.Emitter(
            center_xy=(0.0, 0.0),
            emit_controller=ludi.EmitMaintainCount(20),
            particle_factory=lambda emitter: AnimatedAlphaParticle(
                filename_or_texture=random.choice(STAR_TEXTURES),
                change_xy=(0.0, 0.0),
                start_alpha=0,
                duration1=random.uniform(2.0, 6.0),
                mid_alpha=128,
                duration2=random.uniform(2.0, 6.0),
                end_alpha=0,
                center_xy=ludi.rand_in_rect((0.0, 0.0), SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        )
        self.emitters.append(stars)

        self.cloud = ludi.Emitter(
            center_xy=(50, 500),
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
        self.emitters.append(self.cloud)

    def launch_firework(self, delta_time):
        launchers = (
            self.launch_random_firework,
            self.launch_ringed_firework,
            self.launch_sparkle_firework,
        )
        random.choice(launchers)(delta_time)
        pyglet.clock.schedule_once(self.launch_firework, random.uniform(LAUNCH_INTERVAL_MIN, LAUNCH_INTERVAL_MAX))

    def launch_random_firework(self, _delta_time):
        """Simple firework that explodes in a random color"""
        rocket = make_rocket(self.explode_firework)
        self.emitters.append(rocket)

    def launch_ringed_firework(self, _delta_time):
        """"Firework that has a basic explosion and a ring of sparks of a different color"""
        rocket = make_rocket(self.explode_ringed_firework)
        self.emitters.append(rocket)

    def launch_sparkle_firework(self, _delta_time):
        """Firework which has sparks that sparkle"""
        rocket = make_rocket(self.explode_sparkle_firework)
        self.emitters.append(rocket)

    def launch_spinner(self, _delta_time):
        """Start the spinner that throws sparks"""
        spinner1 = make_spinner()
        spinner2 = make_spinner()
        spinner2.angle = 180
        self.emitters.append(spinner1)
        self.emitters.append(spinner2)

    def explode_firework(self, prev_emitter):
        """Actions that happen when a firework shell explodes, resulting in a typical firework"""
        self.emitters.append(make_puff(prev_emitter))
        self.emitters.append(make_flash(prev_emitter))

        spark_texture = random.choice(SPARK_TEXTURES)
        sparks = ludi.Emitter(
            center_xy=prev_emitter.get_pos(),
            emit_controller=ludi.EmitBurst(random.randint(30, 40)),
            particle_factory=lambda emitter: ludi.FadeParticle(
                filename_or_texture=spark_texture,
                change_xy=ludi.rand_in_circle((0.0, 0.0), 9.0),
                lifetime=random.uniform(0.5, 1.2),
                mutation_callback=firework_spark_mutator
            )
        )
        self.emitters.append(sparks)

    def explode_ringed_firework(self, prev_emitter):
        """Actions that happen when a firework shell explodes, resulting in a ringed firework"""
        self.emitters.append(make_puff(prev_emitter))
        self.emitters.append(make_flash(prev_emitter))

        spark_texture, ring_texture = random.choice(SPARK_PAIRS)
        sparks = ludi.Emitter(
            center_xy=prev_emitter.get_pos(),
            emit_controller=ludi.EmitBurst(25),
            particle_factory=lambda emitter: ludi.FadeParticle(
                filename_or_texture=spark_texture,
                change_xy=ludi.rand_in_circle((0.0, 0.0), 8.0),
                lifetime=random.uniform(0.55, 0.8),
                mutation_callback=firework_spark_mutator
            )
        )
        self.emitters.append(sparks)

        ring = ludi.Emitter(
            center_xy=prev_emitter.get_pos(),
            emit_controller=ludi.EmitBurst(20),
            particle_factory=lambda emitter: ludi.FadeParticle(
                filename_or_texture=ring_texture,
                change_xy=ludi.rand_on_circle((0.0, 0.0), 5.0) + ludi.rand_in_circle((0.0, 0.0), 0.25),
                lifetime=random.uniform(1.0, 1.6),
                mutation_callback=firework_spark_mutator
            )
        )
        self.emitters.append(ring)

    def explode_sparkle_firework(self, prev_emitter):
        """Actions that happen when a firework shell explodes, resulting in a sparkling firework"""
        self.emitters.append(make_puff(prev_emitter))
        self.emitters.append(make_flash(prev_emitter))

        spark_texture = random.choice(SPARK_TEXTURES)
        sparks = ludi.Emitter(
            center_xy=prev_emitter.get_pos(),
            emit_controller=ludi.EmitBurst(random.randint(30, 40)),
            particle_factory=lambda emitter: AnimatedAlphaParticle(
                filename_or_texture=spark_texture,
                change_xy=ludi.rand_in_circle((0.0, 0.0), 9.0),
                start_alpha=255,
                duration1=random.uniform(0.6, 1.0),
                mid_alpha=0,
                duration2=random.uniform(0.1, 0.2),
                end_alpha=255,
                mutation_callback=firework_spark_mutator
            )
        )
        self.emitters.append(sparks)

    def update(self, delta_time):
        # prevent list from being mutated (often by callbacks) while iterating over it
        emitters_to_update = self.emitters.copy()
        # update cloud
        if self.cloud.center_x > SCREEN_WIDTH:
            self.cloud.center_x = 0
        # update
        for e in emitters_to_update:
            e.update()
        # remove emitters that can be reaped
        to_del = [e for e in emitters_to_update if e.can_reap()]
        for e in to_del:
            self.emitters.remove(e)

    def draw(self):
        for e in self.emitters:
            e.draw()
        ludi.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, 25, 0, ludi.color.DARK_GREEN)
        mid = SCREEN_WIDTH / 2
        ludi.draw_lrtb_rectangle_filled(mid - 2, mid + 2, SPINNER_HEIGHT, 10, ludi.color.DARK_BROWN)

    def on_key_press(self, key, modifiers):
        if key == ludi.key.ESCAPE:
            ludi.close_window()


def firework_spark_mutator(particle: ludi.FadeParticle):
    """mutation_callback shared by all fireworks sparks"""
    # gravity
    particle.change_y += -0.03
    # drag
    particle.change_x *= 0.92
    particle.change_y *= 0.92


def rocket_smoke_mutator(particle: ludi.LifetimeParticle):
    particle.scale = ludi.lerp(0.5, 3.0, particle.lifetime_elapsed / particle.lifetime_original)

def install(app):
    app.add_page(FireworksPage, "fireworks", "Fireworks")
