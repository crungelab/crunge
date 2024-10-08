import ctypes

from pyglet import gl, clock
from pyglet.window import key, mouse

import moderngl

from crunge import imgui
from ...util import compute_framebuffer_scale
from ...renderer import Renderer


class ModernGLRenderer(Renderer):

    VERTEX_SHADER_SRC = """
        #version 330
        uniform mat4 ProjMtx;
        in vec2 Position;
        in vec2 UV;
        in vec4 Color;
        out vec2 Frag_UV;
        out vec4 Frag_Color;
        void main() {
            Frag_UV = UV;
            Frag_Color = Color;
            gl_Position = ProjMtx * vec4(Position.xy, 0, 1);
        }
    """
    FRAGMENT_SHADER_SRC = """
        #version 330
        uniform sampler2D Texture;
        in vec2 Frag_UV;
        in vec4 Frag_Color;
        out vec4 Out_Color;
        void main() {
            Out_Color = (Frag_Color * texture(Texture, Frag_UV.st));
        }
    """

    def __init__(self, *args, **kwargs):
        self._prog = None
        self._fbo = None
        self._font_texture = None
        self._vertex_buffer = None
        self._index_buffer = None
        self._vao = None
        self._textures = {}
        self.wnd = kwargs.get("wnd")
        self.ctx = self.wnd.ctx if self.wnd and self.wnd.ctx else kwargs.get("ctx")

        if not self.ctx:
            raise ValueError("Missing moderngl context")

        assert isinstance(self.ctx, moderngl.context.Context)

        super().__init__()

        if "display_size" in kwargs:
            self.io.display_size = kwargs.get("display_size")

    def register_texture(self, texture: moderngl.Texture):
        """Make the imgui renderer aware of the texture"""
        self._textures[texture.glo] = texture

    def remove_texture(self, texture: moderngl.Texture):
        """Remove the texture from the imgui renderer"""
        del self._textures[texture.glo]

    def refresh_font_texture(self):
        pixels, width, height, bpp = self.io.fonts.get_tex_data_as_rgba32()

        if self._font_texture:
            self.remove_texture(self._font_texture)
            self._font_texture.release()

        self._font_texture = self.ctx.texture((width, height), bpp, data=pixels)
        self.register_texture(self._font_texture)
        self.io.fonts.tex_id = self._font_texture.glo
        self.io.fonts.clear_tex_data()

    def _create_device_objects(self):
        self._prog = self.ctx.program(
            vertex_shader=self.VERTEX_SHADER_SRC,
            fragment_shader=self.FRAGMENT_SHADER_SRC,
        )
        self.projMat = self._prog["ProjMtx"]
        self._prog["Texture"].value = 0
        self._vertex_buffer = self.ctx.buffer(reserve=imgui.VERTEX_SIZE * 65536)
        self._index_buffer = self.ctx.buffer(reserve=imgui.INDEX_SIZE * 65536)
        self._vao = self.ctx.vertex_array(
            self._prog,
            [(self._vertex_buffer, "2f 2f 4f1", "Position", "UV", "Color"),],
            index_buffer=self._index_buffer,
            index_element_size=imgui.INDEX_SIZE,
        )

    def render(self, draw_data):
        io = self.io
        display_width, display_height = io.display_size
        fb_width = int(display_width * io. display_framebuffer_scale[0])
        fb_height = int(display_height * io. display_framebuffer_scale[1])

        if fb_width == 0 or fb_height == 0:
            return

        self.projMat.value = (
            2.0 / display_width,
            0.0,
            0.0,
            0.0,
            0.0,
            2.0 / -display_height,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            0.0,
            -1.0,
            1.0,
            0.0,
            1.0,
        )

        draw_data.scale_clip_rects(io.display_framebuffer_scale)

        self.ctx.enable_only(moderngl.BLEND)
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self._font_texture.use()

        for commands in draw_data.cmd_lists:
            # Write the vertex and index buffer data without copying it
            self._vertex_buffer.write(commands.vtx_buffer_data)
            self._index_buffer.write(commands.idx_buffer_data)

            idx_pos = 0
            for command in commands:
                texture = self._textures.get(command.texture_id)
                if texture is None:
                    raise ValueError(
                        (
                            "Texture {} is not registered. Please add to renderer using "
                            "register_texture(..). "
                            "Current textures: {}".format(
                                command.texture_id, list(self._textures)
                            )
                        )
                    )

                texture.use(0)

                x, y, z, w = command.clip_rect
                self.ctx.scissor = int(x), int(fb_height - w), int(z - x), int(w - y)
                self._vao.render(
                    moderngl.TRIANGLES, vertices=command.elem_count, first=idx_pos
                )
                idx_pos += command.elem_count

        self.ctx.scissor = None

    def _invalidate_device_objects(self):
        if self._font_texture:
            self._font_texture.release()
        if self._vertex_buffer:
            self._vertex_buffer.release()
        if self._index_buffer:
            self._index_buffer.release()
        if self._vao:
            self._vao.release()
        if self._prog:
            self._prog.release()

        self.io.fonts.texture_id = 0
        self._font_texture = None


class ModernGLGuiBase:
    def __init__(self, window):
        self.wnd = window

    def _map_keys(self):
        keys = self.wnd.keys

        self.REVERSE_KEY_MAP = {
            keys.TAB: imgui.KEY_TAB,
            keys.LEFT: imgui.KEY_LEFT_ARROW,
            keys.RIGHT: imgui.KEY_RIGHT_ARROW,
            keys.UP: imgui.KEY_UP_ARROW,
            keys.DOWN: imgui.KEY_DOWN_ARROW,
            keys.PAGE_UP: imgui.KEY_PAGE_UP,
            keys.PAGE_DOWN: imgui.KEY_PAGE_DOWN,
            keys.HOME: imgui.KEY_HOME,
            keys.END: imgui.KEY_END,
            keys.DELETE: imgui.KEY_DELETE,
            keys.SPACE: imgui.KEY_SPACE,
            keys.BACKSPACE: imgui.KEY_BACKSPACE,
            keys.ENTER: imgui.KEY_ENTER,
            keys.ESCAPE: imgui.KEY_ESCAPE,
            keys.A: imgui.KEY_A,
            keys.C: imgui.KEY_C,
            keys.V: imgui.KEY_V,
            keys.X: imgui.KEY_X,
            keys.Y: imgui.KEY_Y,
            keys.Z: imgui.KEY_Z,
        }

        for value in self.REVERSE_KEY_MAP.values():
            self.io.set_key_map(value, value)

    def resize(self, width: int, height: int):
        self.io.display_size = (
            self.wnd.viewport_width / self.wnd.pixel_ratio,
            self.wnd.viewport_height / self.wnd.pixel_ratio,
        )

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key in self.REVERSE_KEY_MAP:
                self.io.set_key_down(self.REVERSE_KEY_MAP[key], True)
        else:
            if key in self.REVERSE_KEY_MAP:
                self.io.set_key_down(self.REVERSE_KEY_MAP[key], False)

    def _mouse_pos_viewport(self, x, y):
        """Make sure mouse coordinates are correct with black borders"""
        return (
            int(
                x
                - (self.wnd.width - self.wnd.viewport_width / self.wnd.pixel_ratio) / 2
            ),
            int(
                y
                - (self.wnd.height - self.wnd.viewport_height / self.wnd.pixel_ratio)
                / 2
            ),
        )

    def mouse_position_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

    def mouse_drag_event(self, x, y, dx, dy):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if self.wnd.mouse_states.left:
            self.io.set_mouse_down(0, True)

        if self.wnd.mouse_states.right:
            self.io.set_mouse_down(1, True)

        if self.wnd.mouse_states.middle:
            self.io.set_mouse_down(2, True)

    def mouse_press_event(self, x, y, button):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.set_mouse_down(0, True)

        if button == self.wnd.mouse.right:
            self.io.set_mouse_down(1, True)

        if button == self.wnd.mouse.middle:
            self.io.set_mouse_down(2, True)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.io.mouse_pos = self._mouse_pos_viewport(x, y)

        if button == self.wnd.mouse.left:
            self.io.set_mouse_down(0, False)

        if button == self.wnd.mouse.right:
            self.io.set_mouse_down(1, False)

        if button == self.wnd.mouse.middle:
            self.io.set_mouse_down(2, False)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.io.mouse_wheel = y_offset

    def unicode_char_entered(self, char):
        io = imgui.get_io()
        io.add_input_character(ord(char))


class ModernGLGui(ModernGLGuiBase):
    def __init__(self, window, attach_callbacks=True):
        super().__init__(window)
        self.window = window
        self.context = imgui.create_context()
        imgui.set_current_context(self.context)
        self.io = imgui.get_io()
        self.renderer = ModernGLRenderer(wnd=window)

        self.io.display_size = self.wnd.size
        self.io.display_framebuffer_scale = self.wnd.pixel_ratio, self.wnd.pixel_ratio

        self._map_keys()

        '''
        if attach_callbacks:
            print('attach')
            # register event methods
            self.wnd.resize_func = self.resize
            #self.wnd.iconify_func = self.iconify
            self.wnd.key_event_func = self.key_event
            self.wnd.mouse_position_event_func = self.mouse_position_event
            self.wnd.mouse_drag_event_func = self.mouse_drag_event
            self.wnd.mouse_scroll_event_func = self.mouse_scroll_event
            self.wnd.mouse_press_event_func = self.mouse_press_event
            self.wnd.mouse_release_event_func = self.mouse_release_event
            self.wnd.unicode_char_entered_func = self.unicode_char_entered
            print(self.wnd.__dict__)
            #self.wnd.close_func = self.close
        '''

    def draw(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
