from loguru import logger

from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.widget.label import Label

from ..trial import Trial


class LabelTrial(Trial):
    def reset(self):
        super().reset()
        self.view.ui.attach(Label("Hello, World!"))

    '''
    def draw(self, renderer: Renderer):
        if imgui.begin("Panel"):
            imgui.text("This is a panel widget.")
            imgui.end()

        super().draw(renderer)
    '''

def main():
    LabelTrial().run()


if __name__ == "__main__":
    main()
