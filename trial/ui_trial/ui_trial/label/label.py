from loguru import logger

from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.widget.label import Label

from ..trial import Trial


class LabelTrial(Trial):
    def reset(self):
        super().reset()
        self.view.ui.add_child(Label("Hello, World!"))

def main():
    LabelTrial().run()


if __name__ == "__main__":
    main()
