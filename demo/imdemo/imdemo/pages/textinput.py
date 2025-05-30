from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class TextInputPage(Page):
    def reset(self):
        self.text_val = 'Type your message here.'

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        changed, self.text_val = imgui.input_text(
            'Text',
            self.text_val,
            256
        )
        imgui.text('You wrote:')
        imgui.same_line()
        imgui.text(self.text_val)
        imgui.end()
        super().draw(renderer)

class MultiTextInputPage(Page):
    def reset(self):
        self.text_val = 'Type your message here.'

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        changed, self.text_val = imgui.input_text_multiline(
            'Message',
            self.text_val,
            2056,
            (0,0),
            0
        )
        imgui.text('You wrote:')
        imgui.same_line()
        imgui.text(self.text_val)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(TextInputPage, "textinput", "Text Input"))
    app.add_channel(PageChannel(MultiTextInputPage, "multitextinput", "Multiline Text Input"))
