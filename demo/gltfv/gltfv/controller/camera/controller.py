import glfw

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

    def on_cursor_pos(self, window, xpos, ypos):
        if not self.mouse_captured:
            return
        self.process_mouse_movement(xpos, ypos)

    def on_mouse_button(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                self.mouse_captured = True
                self.first_mouse = True
            elif action == glfw.RELEASE:
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                self.mouse_captured = False


    def on_key(self, window, key, scancode, action, mods):
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.process_keyboard('FORWARD', self.delta_time)
        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.process_keyboard('BACKWARD', self.delta_time)