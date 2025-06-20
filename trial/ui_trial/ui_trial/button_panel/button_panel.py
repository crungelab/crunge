from loguru import logger

from crunge import imgui
from crunge import yoga
from crunge.yoga import StyleBuilder
from crunge.engine import Renderer
from crunge.engine.widget.panel import Panel
from crunge.engine.widget.button import Button

from ..trial import Trial


class ButtonsTrial(Trial):
    def reset(self):
        super().reset()

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
        panel.attach(button1)

        button2 = Button(
            "Button 2",
            style=button_style,
            on_click=lambda: logger.info("Button 2 clicked!"),
        )
        panel.attach(button2)

        ui = self.view.ui

        ui.layout.set_width_percent(100)
        ui.layout.set_height_percent(100)
        ui.layout.set_justify_content(yoga.Justify.CENTER)
        ui.layout.set_align_items(yoga.Align.CENTER)

        ui.attach(panel)


def main():
    ButtonsTrial().run()


if __name__ == "__main__":
    main()
