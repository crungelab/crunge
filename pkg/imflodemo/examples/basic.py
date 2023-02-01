import arcade

from crunge import imgui
from imgui.impl.arcade import ArcadeGui

import imnodes

class MyGui(ArcadeGui):
    def __init__(self, window):
        super().__init__(window)
        imnodes.create_context()
        imnodes.push_attribute_flag(imnodes.ATTRIBUTE_FLAGS_ENABLE_LINK_DETACH_WITH_DRAG_CLICK)
        io = imnodes.get_io()
        #TODO:Looks too scary to wrap.
        #io.link_detach_with_modifier_click.modifier = imgui.get_io().key_ctrl



class App(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Main Window", resizable=True)
        self.gui = MyGui(self)
        self.links = []
        self.link_id = 0

    def add_link(self, id1, id2):
        self.links.append((self.link_id, id1, id2))
        self.link_id += 1

    def on_draw(self):
        arcade.start_render()
        imgui.new_frame()

        imgui.set_next_window_pos((16, 32), imgui.COND_FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.COND_FIRST_USE_EVER )

        imgui.begin('Nodes')

        imnodes.begin_node_editor()

        # Node 1
        imnodes.begin_node(1)
        
        imnodes.begin_node_title_bar()
        imgui.text('Output')
        imnodes.end_node_title_bar()

        imnodes.begin_output_attribute(1)
        imgui.text('output')
        imnodes.end_output_attribute()

        imnodes.end_node()

        # Node 2
        imnodes.begin_node(2)
        
        imnodes.begin_node_title_bar()
        imgui.text('Input')
        imnodes.end_node_title_bar()

        imnodes.begin_input_attribute(2)
        imgui.text('input')
        imnodes.end_input_attribute()

        imnodes.end_node()
            
        for link in self.links:
            imnodes.link(link[0], link[1], link[2])

        imnodes.end_node_editor()

        if (result := imnodes.is_link_created(0,0))[0]:
            print('output:  ', result[1])
            print('input:  ', result[2])
            self.add_link(result[1], result[2])

        if (result := imnodes.is_link_destroyed(0))[0]:
            print('destroyed: ', result[1])

        imgui.end()
        #imgui.show_metrics_window()
        imgui.end_frame()
        self.gui.render()

app = App()

arcade.run()
