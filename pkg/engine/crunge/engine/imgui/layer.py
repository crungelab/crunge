import os, sys

from loguru import logger
import glm

from crunge import engine
from crunge.engine import Renderer

from crunge import sdl
from crunge import imgui
from crunge.imgui import Key

from ..layer import Layer

from .vu import ImGuiVu
from .scancode_map import scancode_map


def compute_framebuffer_scale(window_size, frame_buffer_size):
    win_width, win_height = window_size
    fb_width, fb_height = frame_buffer_size

    if win_width != 0 and win_width != 0:
        return fb_width / win_width, fb_height / win_height

    return 1.0, 1.0

class ImGuiLayer(Layer):
    context = None
    vu = None

    def __init__(self):
        super().__init__("ImGuiLayer")
        self.last_mouse = glm.vec2(-sys.float_info.max, -sys.float_info.max)

    def create(self, view: engine.View):
        super().create(view)
        if not self.context:
            ImGuiLayer.context = imgui.create_context()
            imgui.set_current_context(self.context)
            imgui.style_colors_dark()

        self.io = imgui.get_io()
        self.vu = ImGuiVu()
        self._set_pixel_ratio()
        return self

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self._set_pixel_ratio()

    def _set_pixel_ratio(self):
        window_size = self.window.get_size()
        self.io.display_size = window_size

        framebuffer_size = self.window.get_framebuffer_size()
        pixel_ratio = compute_framebuffer_scale(window_size, framebuffer_size)
        self.io.display_framebuffer_scale = pixel_ratio

    def pre_draw(self, renderer: Renderer):
        #logger.debug("ImGuiLayer.pre_draw")
        imgui.new_frame()
        super().pre_draw(renderer)

    def post_draw(self, renderer: Renderer):
        #logger.debug("ImGuiLayer.post_draw")
        imgui.end_frame()
        super().post_draw(renderer)

    def on_text(self, event: sdl.TextInputEvent):
        #logger.debug(f"text: {event.text}")
        self.io.add_input_characters_utf8(event.text)

    def on_key(self, event: sdl.KeyboardEvent):
        #logger.debug(f"scan code: {event.scancode}")
        if not event.scancode in scancode_map:
            logger.debug(f"scan code not mapped: {event.scancode}")
            return

        down = event.type == sdl.EventType.KEY_DOWN

        self.update_modifiers()

        self.io.add_key_event(scancode_map[event.scancode], down)

        if self.io.want_capture_keyboard:
            return self.EVENT_HANDLED

    '''
    def on_key(self, event: sdl.KeyboardEvent):
        logger.debug(f"key: {event.key}")
        if event.key in key_map:
            self.io.add_key_event(key_map.get(event.key), event.state == 1)
        else:
            logger.debug(f"key not mapped: {event.key}")
        self.update_modifiers()
        if self.io.want_capture_keyboard:
            return self.EVENT_HANDLED
    '''

    def update_modifiers(self):
        mod_state = sdl.get_mod_state()
        self.io.add_key_event(Key.MOD_CTRL, mod_state & sdl.KMOD_CTRL)
        self.io.add_key_event(Key.MOD_SHIFT, mod_state & sdl.KMOD_SHIFT)
        self.io.add_key_event(Key.MOD_ALT, mod_state & sdl.KMOD_ALT)
        self.io.add_key_event(Key.MOD_SUPER, mod_state & sdl.KMOD_GUI)

    def on_mouse_enter(self, event: sdl.WindowEvent):
        super().on_mouse_enter(event)
        self.io.add_mouse_pos_event(self.last_mouse.x, self.last_mouse.y)

    def on_mouse_leave(self, event: sdl.WindowEvent):
        super().on_mouse_leave(event)
        last_mouse = self.io.mouse_pos
        self.last_mouse = glm.vec2(last_mouse[0], last_mouse[1])
        self.io.add_mouse_pos_event(-sys.float_info.max, -sys.float_info.max)

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        super().on_mouse_motion(event)
        x, y = event.x, event.y
        self.io.add_mouse_pos_event(x, y)
        self.last_mouse = glm.vec2(x, y)
        if self.io.want_capture_mouse:
            return self.EVENT_HANDLED

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button == 1:
            button = 0
        elif event.button == 3:
            button = 1
        elif event.button == 2:
            button = 2
        action = event.state == 1
        if button < 3:
            self.io.add_mouse_button_event(button, action)
        if self.io.want_capture_mouse:
            return self.EVENT_HANDLED

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        x, y = event.x, event.y
        self.io.add_mouse_wheel_event(x, y)
        if self.io.want_capture_mouse:
            return self.EVENT_HANDLED
            
