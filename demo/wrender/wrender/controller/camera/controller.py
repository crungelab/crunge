from loguru import logger

from crunge import sdl

from ..controller import Controller
from ...camera import Camera


class CameraController(Controller):
    def __init__(self, window, camera: Camera):
        super().__init__(window)
        self.camera = camera

    @property
    def position(self):
        return self.camera.position
    
    @position.setter
    def position(self, value):
        self.camera.position = value

    @property
    def orientation(self):
        return self.camera.orientation
    
    @orientation.setter
    def orientation(self, value):
        self.camera.orientation = value

    def process_mouse_movement(self, xpos, ypos):
        pass

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        if not self.mouse_captured:
            return
        self.process_mouse_movement(event.x, event.y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        logger.debug(f"mouse button: button={event.button}, state={event.state}")
        if event.button == 1:
            if event.state:
                logger.debug("Capturing mouse")
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                self.mouse_captured = True
                self.first_mouse = True
            else:
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                self.mouse_captured = False

    def process_keyboard(self, direction, delta_time):
        pass

    def on_key(self, event: sdl.KeyboardEvent):
        logger.debug(f"key: {event.keysym.sym}")
        key = event.keysym.sym
        state = event.state
        #if key == sdl.SDLK_w and (state == 1 or action == glfw.REPEAT):
        if key == sdl.SDLK_w and (state == 1 or event.repeat):
            self.process_keyboard('FORWARD', self.delta_time)
        #if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
        if key == sdl.SDLK_s and (state == 1 or event.repeat):
            self.process_keyboard('BACKWARD', self.delta_time)