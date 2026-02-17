from loguru import logger
import glm

from crunge import sdl
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine import Controller
    
CAMERA_MOVEMENT_SPEED = 500.0
LERP_SPEED = 10.0  # Higher = snappier, Lower = smoother/floatier

class ScrollingDemoController(Controller):
    def __init__(self, camera: Camera2D):
        super().__init__()
        self.camera = camera
        self.velocity = glm.vec2(0, 0)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def update(self, delta_time: float):
        target_velocity = glm.vec2(0, 0)

        if self.left_pressed:
            target_velocity.x -= CAMERA_MOVEMENT_SPEED
        if self.right_pressed:
            target_velocity.x += CAMERA_MOVEMENT_SPEED
        if self.up_pressed:
            target_velocity.y += CAMERA_MOVEMENT_SPEED
        if self.down_pressed:
            target_velocity.y -= CAMERA_MOVEMENT_SPEED

        # Lerp current velocity toward target for smooth acceleration/deceleration
        t = min(LERP_SPEED * delta_time, 1.0)
        self.velocity = glm.mix(self.velocity, target_velocity, t)

        # Snap to zero to avoid endless creep
        if glm.length(self.velocity) < 0.5:
            self.velocity = glm.vec2(0, 0)

        self.camera.position += self.velocity * delta_time

        #logger.debug(f"Camera velocity: {self.velocity}, position: {self.camera.position}")

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat

        #logger.debug(f"Key event: {key}, down: {down}, repeat: {repeat}")

        match key:
            case sdl.SDLK_w:
                self.up_pressed = down
            case sdl.SDLK_s:
                self.down_pressed = down
            case sdl.SDLK_a:
                self.left_pressed = down
            case sdl.SDLK_d:
                self.right_pressed = down