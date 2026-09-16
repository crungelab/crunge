import math

from loguru import logger

from crunge.engine import App
from crunge.demo import PageChannel

from ..page import Page

from crunge.engine.ui.button import Button
from crunge.yoga import StyleBuilder


class ButtonPage(Page):
    def setup(self):
        super().setup()
        self.ui.add_child(
            Button(
                "Hello, World!",
                style=StyleBuilder().size(200, 50).build(),
            )
        )


def install(app: App):
    app.add_channel(PageChannel(ButtonPage, "button", "Button"))
