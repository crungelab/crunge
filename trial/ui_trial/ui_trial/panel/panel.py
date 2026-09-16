from loguru import logger

from crunge import imgui
from crunge import yoga
from crunge.engine import Renderer
from crunge.engine.ui.panel import Panel
from crunge.yoga import StyleBuilder
from ..trial import Trial


class PanelTrial(Trial):
    def setup(self):
        super().setup()
        panel = Panel(style=StyleBuilder().size(400, 300).build())

        self.display.ui.add_child(panel)


def main():
    PanelTrial().run()


if __name__ == "__main__":
    main()
