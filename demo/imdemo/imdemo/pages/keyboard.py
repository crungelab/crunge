from loguru import logger

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer, App
from crunge.engine.imgui.key_map import key_map
from crunge.demo import Page, PageChannel


class KeyboardPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        self.key = None

    def _draw(self):
        imgui.begin(self.title)

        imgui.text("Press any key to see its state")
        if self.key is not None:
            imgui.label_text(str(self.key), "key")
            imgui.label_text(str(imgui.get_key_name(self.key)), "key name")
            imgui.label_text(str(imgui.is_key_down(self.key)), "is down")
            imgui.label_text(str(imgui.is_key_pressed(self.key)), "is pressed")
            imgui.label_text(str(imgui.is_key_released(self.key)), "is released")
        else:
            imgui.text("No key pressed yet")

        imgui.end()
        super()._draw()

    def on_key(self, event: sdl.KeyboardEvent):
        self.key = key_map[event.key]
        
        down = event.type == sdl.EventType.KEY_DOWN


def install(app: App):
    app.add_channel(PageChannel(KeyboardPage, "keyboard", "Keyboard"))
