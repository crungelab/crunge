from contextlib import contextmanager

from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


lorem_ipsum = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
'''

'''
class TabItem:
    def __init__(self, name):
        self.name = name
        self.p_open = True
    def __enter__(self):
        self.value, self.p_open = imgui.begin_tab_item(self.name, self.p_open)
        return self.value
    def __exit__(self, type, value, traceback):
        imgui.end_tab_item()
'''


@contextmanager
def tab_item(name, p_open):
    result, p_open = imgui.begin_tab_item(name, p_open)
    if not result:
        return
    try:
        yield p_open
    finally:
        imgui.end_tab_item()

class TabsPage(Page):
    def reset(self):
        self.tabs = [True, True]
        self.color = 1,1,1

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        imgui.begin_child("item view", (0, -imgui.get_frame_height_with_spacing())) #Leave room for 1 line below us
        imgui.text("Settings")
        imgui.separator()

        if imgui.begin_tab_bar("##Tabs"):
            if imgui.begin_tab_item("Standard settings", self.tabs[0])[0]:
                imgui.text_wrapped(lorem_ipsum)
                imgui.end_tab_item()

            if imgui.begin_tab_item("Render settings", self.tabs[1])[0]:
                _, self.color = imgui.color_picker3("Background color", self.color)
                imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end_child()

        imgui.text("outside region")
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(TabsPage, "tabs", "Tabs"))
