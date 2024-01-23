from crunge import imgui
from crunge.imgui import rel
from crunge.imgui.impl.ludi import LudiGui

from experiments.gig.gui import LudiPortalGui

import ludi

class InnerGui(LudiPortalGui):
    def draw(self):
        imgui.set_current_context(self.context)
        #self.io.display_framebuffer_scale = (self.zoom, self.zoom)
        #self.io.font_global_scale = self.zoom
        imgui.new_frame()
        
        imgui.set_next_window_size((500,500))
        imgui.begin('Portal')

        pos_x, pos_y = self.io.mouse_pos
        sz = 10

        draw_list = imgui.get_foreground_draw_list()
        draw_list.add_rect_filled((pos_x, pos_y), (pos_x+sz, pos_y+sz), imgui.get_color_u32(0))

        sz = 20
        draw_list = imgui.get_window_draw_list()
        rgba_color = imgui.get_color_u32((1, 1, 1, 1))
        for i in range(0, imgui.COL_COUNT):
            name = imgui.get_style_color_name(i)
            color = imgui.get_color_u32(imgui.get_style_color_vec4(i))
            p1 = rel(0, i*10)
            p2 = (p1[0] + sz, p1[1] + sz)
            draw_list.add_rect_filled(p1, p2, color)
            
            p1 = rel(20, i*10)
            draw_list.add_text(p1, rgba_color, name)

        imgui.end()

        imgui.begin('Portal##2')
        imgui.button("Button 3")
        imgui.button("Button 4")
        imgui.end()

        imgui.end_frame()
        super().draw()

class App(ludi.Window):
    def __init__(self):
        super().__init__(1280, 640, 'Gui in Gui Experiment', resizable=True)
        self.gui = LudiGui(self)
        self.inner_gui = InnerGui(self)

    def on_draw(self):
        ludi.start_render()

        imgui.set_current_context(self.gui.context)
        imgui.new_frame()

        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")

        self.inner_gui.position = imgui.get_cursor_screen_pos()
        size = imgui.get_content_region_max()
        self.inner_gui.size = size
        imgui.invisible_button("Blah", size)
        self.inner_gui.hovered = imgui.is_item_hovered()

        def cb(renderer, draw_data, draw_list, cmd, user_data):
            self.inner_gui.draw()
            imgui.set_current_context(self.gui.context)

        draw_list = imgui.get_window_draw_list()
        draw_list.add_callback(cb, None)

        imgui.end()

        imgui.show_metrics_window()
        imgui.end_frame()

        self.gui.render()

app = App()
ludi.run()
