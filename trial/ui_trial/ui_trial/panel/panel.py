from loguru import logger

from crunge import imgui
from crunge import yoga
from crunge.engine import Renderer
from crunge.engine.widget.panel import Panel
from crunge.yoga import StyleBuilder
from ..trial import Trial


class PanelTrial(Trial):
    def reset(self):
        super().reset()
        panel = Panel(style=StyleBuilder().size(400, 300).build())

        self.view.ui.attach(panel)


def main():
    PanelTrial().run()


if __name__ == "__main__":
    main()
