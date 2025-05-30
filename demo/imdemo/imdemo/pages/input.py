from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Input(Page):
    def reset(self):
        self.test_input = 0

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        imgui.text("This is the test window.")
        changed, self.test_input = imgui.input_int("Integer", self.test_input)

        imgui.end()

        # ludi.draw_text(str(self.test_input), 0, 0, ludi.color.WHITE_SMOKE, 64)
        super().draw(renderer)


class InputDouble(Page):
    def reset(self):
        self.double_val = 3.14159265358979323846

    def draw(self, renderer: Renderer):
        imgui.begin("Test Window")

        imgui.text("This is the test window.")
        changed, self.double_val = imgui.input_double("Double:", self.double_val)
        imgui.text("You wrote: %d" % self.double_val)

        imgui.end()

        # ludi.draw_text(str(self.double_val), 0, 0, ludi.color.WHITE_SMOKE, 64)
        super().draw(renderer)


class InputFloat(Page):
    def reset(self):
        self.float_val = 0.4

    def draw(self, renderer: Renderer):
        imgui.begin("Test Window")

        imgui.text("This is the test window.")
        changed, self.float_val = imgui.input_float("Float:", self.float_val)
        imgui.text("You wrote: %f" % self.float_val)
        imgui.end()

        # ludi.draw_text(str(self.float_val), 0, 0, ludi.color.WHITE_SMOKE, 64)
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(Input, "input", "Input"))
    app.add_channel(PageChannel(InputDouble, "inputdouble", "Input Double"))
    app.add_channel(PageChannel(InputFloat, "inputfloat", "Input Float"))
