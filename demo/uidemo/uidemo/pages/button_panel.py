import math

from loguru import logger

from crunge import yoga

from crunge.engine import App
from crunge.demo import PageChannel

from ..page import Page

from crunge.engine.ui.button import Button
from crunge.engine.ui.panel import Panel
from crunge.yoga import StyleBuilder


class ButtonPanelPage(Page):
    def setup(self):
        super().setup()

        panel = Panel(style=StyleBuilder()
            .size(400, 300)
            .build()
        )

        button_style = StyleBuilder().height(50).margin(yoga.Edge.ALL, 5).build()

        button1 = Button(
            "Button 1",
            style=button_style,
            on_click=lambda: logger.info("Button 1 clicked!"),
        )
        panel.add_child(button1)

        button2 = Button(
            "Button 2",
            style=button_style,
            on_click=lambda: logger.info("Button 2 clicked!"),
        )
        panel.add_child(button2)

        ui = self.ui

        ui.layout.layout_node.set_width_percent(100)
        ui.layout.layout_node.set_height_percent(100)
        ui.layout.layout_node.set_justify_content(yoga.Justify.CENTER)
        ui.layout.layout_node.set_align_items(yoga.Align.CENTER)

        ui.add_child(panel)


def install(app: App):
    app.add_channel(PageChannel(ButtonPanelPage, "button_panel", "Button Panel"))
