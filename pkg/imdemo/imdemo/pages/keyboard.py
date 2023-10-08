from crunge import imgui

from imdemo.page import Page


class KeyboardPage(Page):
    def draw(self):
        imgui.begin(self.title)
        '''
        imgui.label_text(str(imgui.is_key_down()), "is down")
        imgui.label_text(str(imgui.get_key_index()), "index")
        imgui.label_text(str(imgui.is_key_pressed), "is pressed")
        imgui.label_text(str(imgui.is_key_released), "is released")
        '''
        imgui.end()

def install(app):
    app.add_page(KeyboardPage, "keyboard", "Keyboard")
