import math

from loguru import logger

from crunge.engine import App
from crunge.demo import PageChannel

from ..page import Page

from crunge.engine.ui import Button, Text
from crunge.engine.colors import Color, WHITE

from crunge.yoga import StyleBuilder


class ButtonPage(Page):
    def setup(self):
        super().setup()
        self.ui.add_child(
            Button(
                Text("Hello, World!", color=WHITE),
                #style=StyleBuilder().size(200, 50).build(),
                on_pressed=self.on_button_pressed,
            )
        )

    def on_button_pressed(self):
        logger.info("Button pressed!")


def install(app: App):
    app.add_channel(PageChannel(ButtonPage, "button", "Button"))
