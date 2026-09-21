import math

from loguru import logger

from crunge.engine import App
from crunge.demo import PageChannel

from ..page import Page

from crunge.engine.ui.text import Text
from crunge.engine.colors import Color, CYAN

from crunge.yoga import StyleBuilder


class TextPage(Page):
    def setup(self):
        super().setup()
        self.ui.add_child(
            Text(
                "Hello, World!",
                color=CYAN,
                style=StyleBuilder().size(200, 50).build(),
            )
        )


def install(app: App):
    app.add_channel(PageChannel(TextPage, "text", "Text"))
