#from glfw import

class Controller:
    def __init__(self, window):
        self.window = window
        self.mouse_captured = False
        self.delta_time = 0

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self, delta_time: float):
        self.delta_time = delta_time

    def on_cursor_pos(self, window, xpos, ypos):
        pass

    def on_mouse_button(self, window, button, action, mods):
        pass

    def on_scroll(self, window, xoffset, yoffset):
        pass

    def on_key(self, window, key, scancode, action, mods):
        pass