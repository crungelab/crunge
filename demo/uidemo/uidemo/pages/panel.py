import math

from loguru import logger

from crunge.engine import App
from crunge.demo import PageChannel

from ..page import Page

from crunge.engine.ui.panel import Panel
from crunge.yoga import StyleBuilder


class PanelPage(Page):
    def setup(self):
        super().setup()
        panel = Panel(style=StyleBuilder().size(400, 300).build())

        self.ui.add_child(panel)


def install(app: App):
    app.add_channel(PageChannel(PanelPage, "panel", "Panel"))
