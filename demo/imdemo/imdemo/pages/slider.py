from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class FloatSliderPage(Page):
    def reset(self):
        self.value = 88

    def draw(self, renderer: Renderer):
        width = 20
        height = 100

        imgui.begin(self.title)
        changed, self.value = imgui.v_slider_float(
            "vertical slider float",
            (width, height), self.value,
            v_min=0, v_max=100,
            format="%0.3f"
        )
        imgui.text("Changed: %s, Values: %s" % (changed, self.value))
        imgui.end()
        super().draw(renderer)

class IntSliderPage(Page):
    def reset(self):
        self.value = 88

    def draw(self, renderer: Renderer):
        width = 20
        height = 100

        imgui.begin(self.title)
        changed, self.value = imgui.v_slider_int(
            "vertical slider int",
            (width, height), self.value,
            v_min=0, v_max=100,
            format="%d"
        )
        imgui.text("Changed: %s, Values: %s" % (changed, self.value))
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(FloatSliderPage, "floatslider", "Slider - Float")
    app.add_channel(PageChannel(FloatSliderPage, "floatslider", "Slider - Float"))
    #app.add_page(IntSliderPage, "intslider", "Slider - Integer")
    app.add_channel(PageChannel(IntSliderPage, "intslider", "Slider - Integer"))
