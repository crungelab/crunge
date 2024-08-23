import pyglet
pyglet.options['shadow_window']=False

from crunge import imgui
from crunge.imgui.impl.ludi import LudiGui

from crunge import engine

class ChildGui(LudiGui):
    def __init__(self, window):
        super().__init__(window)
        self.title = "Child Gui"
        io = imgui.get_io()
        io.config_flags |= imgui.CONFIG_FLAGS_DOCKING_ENABLE | imgui.CONFIG_FLAGS_VIEWPORTS_ENABLE

    def draw(self):
        imgui.set_current_context(self.context)
        imgui.new_frame()

        imgui.set_next_window_pos((16, 32), imgui.COND_FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.COND_FIRST_USE_EVER )


        imgui.begin(self.title)

        dockspace_id = imgui.get_id(self.title)
        dockspace_flags = imgui.DOCK_NODE_FLAGS_NONE|imgui.DOCK_NODE_FLAGS_PASSTHRU_CENTRAL_NODE
        imgui.dock_space(dockspace_id , (0., 0.), dockspace_flags)

        imgui.end()


        imgui.set_next_window_dock_id(dockspace_id , imgui.COND_FIRST_USE_EVER)


        imgui.begin('Dockable Window#1')
        imgui.begin_child("region", (150, -50), border=True)
        imgui.text("inside region")
        imgui.end_child()
        imgui.text("outside region")
        imgui.end()

        imgui.end_frame()

        super().draw()

class ChildApp(ludi.Window):
    def __init__(self):
        super().__init__(800, 600, "Child Window", resizable=True)
        self.gui = ChildGui(self)

    def draw(self):
        ludi.start_render()
        self.gui.render()


class MyGui(LudiGui):
    def __init__(self, window):
        super().__init__(window)
        self.title = "Parent Gui"
        io = imgui.get_io()
        io.config_flags |= imgui.CONFIG_FLAGS_DOCKING_ENABLE | imgui.CONFIG_FLAGS_VIEWPORTS_ENABLE

    def draw(self):
        imgui.set_current_context(self.context)
        imgui.new_frame()

        imgui.set_next_window_pos( (16, 32), imgui.COND_FIRST_USE_EVER )
        imgui.set_next_window_size( (512, 512), imgui.COND_FIRST_USE_EVER )

        imgui.begin(self.title)

        dockspace_id = imgui.get_id(self.title)
        dockspace_flags = imgui.DOCK_NODE_FLAGS_NONE|imgui.DOCK_NODE_FLAGS_PASSTHRU_CENTRAL_NODE
        imgui.dock_space(dockspace_id , (0., 0.), dockspace_flags)

        imgui.end()


        imgui.set_next_window_dock_id(dockspace_id , imgui.COND_FIRST_USE_EVER)


        imgui.begin('Dockable Window#2')
        imgui.begin_child("region", (150, -50), border=True)
        imgui.text("inside region")
        imgui.end_child()
        imgui.text("outside region")
        imgui.end()
        imgui.show_metrics_window()
        imgui.end_frame()

        super().draw()

class App(ludi.Window):
    def __init__(self):
        super().__init__(800, 600, "Main Window", resizable=True)
        self.gui = MyGui(self)

    def draw(self):
        ludi.start_render()
        self.gui.render()


#app = ChildApp()
app = App()

ludi.run()

#pyglet.app.run()
