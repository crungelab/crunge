from crunge import imgui
from experiments.portal.gui import LudiGui

import ludi

class App(ludi.Window):
    def __init__(self):
        super().__init__(800, 600, 'Portal Experiment', resizable=True)
        self.gui = LudiGui(self)

    def on_draw(self):
        ludi.start_render()

        imgui.new_frame()

        pos_x = 10
        pos_y = 10
        sz = 20
        
        imgui.begin('Portal')

        portal = imgui.get_cursor_screen_pos()
        draw_list = imgui.get_window_draw_list()
        self.gui.push_portal(draw_list, portal)
        region = imgui.get_content_region_max()
        imgui.push_clip_rect((0,0), region, False)
        #draw_list.push_clip_rect_full_screen()
        for i in range(0, imgui.COL_COUNT):
            name = imgui.get_style_color_name(i)
            pos_y = i*20
            draw_list.add_rect_filled((pos_x, pos_y), (pos_x+sz, pos_y+sz), imgui.get_color_u32(i))
            draw_list.add_text((pos_x+32, pos_y), imgui.get_color_u32((1,1,1,1)), name)

        imgui.pop_clip_rect()

        self.gui.pop_portal(draw_list)

        imgui.end()

        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()

        imgui.end_frame()

        self.gui.draw()


app = App()
ludi.run()
