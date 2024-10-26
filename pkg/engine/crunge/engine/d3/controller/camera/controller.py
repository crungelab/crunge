from loguru import logger

from crunge import sdl

from ....dispatcher import DispatchResult

from ..controller import Controller
from ...camera_3d import Camera3D


class CameraController(Controller):
    def __init__(self, window, camera: Camera3D):
        super().__init__(window)
        self.camera = camera
        self.mouse_captured = False
        self.first_mouse = True
        self.mouse_button = 0

    @property
    def width(self):
        return self.window.size.x
    
    @property
    def height(self):
        return self.window.size.y

    @property
    def position(self):
        return self.camera.position
    
    @position.setter
    def position(self, value):
        logger.debug(f"Setting camera position: x={value.x}, y={value.y}, z={value.z}")
        self.camera.position = value

    @property
    def orientation(self):
        return self.camera.orientation
    
    @orientation.setter
    def orientation(self, value):
        self.camera.orientation = value

    def process_mouse_movement(self, xpos, ypos):
        pass

    def on_mouse_motion(self, event: sdl.MouseMotionEvent) -> DispatchResult:
        if not self.mouse_captured:
            return
        self.process_mouse_movement(event.x, event.y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        #logger.debug(f"mouse button: button={event.button}, down={event.down}")
        #if event.button == 1:
        if event.button > 0:
            if event.down:
                #logger.debug("Capturing mouse")
                self.mouse_captured = True
                self.first_mouse = True
                self.mouse_button = event.button
            else:
                self.mouse_captured = False

    def process_keyboard(self, direction, delta_time):
        pass

    def on_key(self, event: sdl.KeyboardEvent):
        #logger.debug(f"key: {event.key}")
        key = event.key
        down = event.down
        repeat = event.repeat
        if key == sdl.SDLK_w and (down or repeat):
            self.process_keyboard('FORWARD', self.delta_time)
        elif key == sdl.SDLK_s and (down or repeat):
            self.process_keyboard('BACKWARD', self.delta_time)
        elif key == sdl.SDLK_a and (down or repeat):
            self.process_keyboard('LEFT', self.delta_time)
        elif key == sdl.SDLK_d and (down or repeat):
            self.process_keyboard('RIGHT', self.delta_time)