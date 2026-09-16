from loguru import logger

from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.ui.label import Label

from ..trial import Trial


class LabelTrial(Trial):
    def setup(self):
        super().setup()
        self.display.ui.add_child(Label("Hello, World!"))

def main():
    LabelTrial().run()


if __name__ == "__main__":
    main()
