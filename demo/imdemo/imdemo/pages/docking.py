from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class DockingPage(Page):
    '''
    def reset(self):
        io = imgui.get_io()
        io.config_flags |= imgui.ConfigFlags.DOCKING_ENABLE
    '''
    
    def _draw(self):
        imgui.begin(self.title, True)

        dockspace_id = imgui.get_id(self.title)
        dockspace_flags = (
            imgui.DockNodeFlags.NONE | imgui.DockNodeFlags.PASSTHRU_CENTRAL_NODE
        )
        imgui.dock_space(dockspace_id, (0.0, 0.0), dockspace_flags)

        imgui.end()

        imgui.set_next_window_dock_id(dockspace_id, imgui.Cond.FIRST_USE_EVER)

        imgui.begin("Dockable Window")

        imgui.begin_child("region", (150, -50), imgui.ChildFlags.BORDERS)
        imgui.text("inside region")
        imgui.end_child()

        imgui.text("outside region")

        imgui.end()
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(DockingPage, "docking", "Docking"))
