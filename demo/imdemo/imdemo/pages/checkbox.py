from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Checkbox(Page):
    def reset(self):
        self.checkbox1_enabled = True
        self.checkbox2_enabled = False

    def draw(self, renderer: Renderer):
        imgui.begin("Example: checkboxes")

        # note: first element of return two-tuple notifies if there was a click
        #       event in currently processed frame and second element is actual
        #       checkbox state.
        _, self.checkbox1_enabled = imgui.checkbox("Checkbox 1", self.checkbox1_enabled)
        _, self.checkbox2_enabled = imgui.checkbox("Checkbox 2", self.checkbox2_enabled)

        imgui.text("Checkbox 1 state value: {}".format(self.checkbox1_enabled))
        imgui.text("Checkbox 2 state value: {}".format(self.checkbox2_enabled))

        imgui.end()
        super().draw(renderer)

class CheckboxFlags(Page):
    def reset(self):
        #self.flags = imgui.WINDOW_FLAGS_NO_RESIZE | imgui.WINDOW_FLAGS_NO_MOVE
        self.flags = imgui.WindowFlags.NO_RESIZE | imgui.WindowFlags.NO_MOVE

    def draw(self, renderer: Renderer):
        imgui.begin("Example: checkboxes for flags", flags=self.flags)

        clicked, self.flags = imgui.checkbox_flags(
            #"No resize", self.flags, imgui.WINDOW_FLAGS_NO_RESIZE
            "No resize", self.flags, imgui.WindowFlags.NO_RESIZE
        )
        clicked, self.flags = imgui.checkbox_flags(
            #"No move", self.flags, imgui.WINDOW_FLAGS_NO_MOVE
            "No move", self.flags, imgui.WindowFlags.NO_MOVE
        )
        clicked, self.flags = imgui.checkbox_flags(
            #"No collapse", self.flags, imgui.WINDOW_FLAGS_NO_COLLAPSE
            "No collapse", self.flags, imgui.WindowFlags.NO_COLLAPSE
        )
        # note: it also allows to use multiple flags at once
        clicked, self.flags = imgui.checkbox_flags(
            "No resize & no move", self.flags,
            #imgui.WINDOW_FLAGS_NO_RESIZE | imgui.WINDOW_FLAGS_NO_MOVE
            imgui.WindowFlags.NO_RESIZE | imgui.WindowFlags.NO_MOVE
        )
        imgui.text("Current flags value: {0:b}".format(self.flags))
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Checkbox, "checkbox", "Checkbox"))
    app.add_channel(PageChannel(CheckboxFlags, "checkboxflags", "CheckboxFlags"))


