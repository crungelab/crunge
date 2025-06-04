from loguru import logger

from crunge.engine import Renderer
from crunge.engine.widget.button import Button
from crunge.yoga import LayoutBuilder

from ..trial import Trial


class ButtonTrial(Trial):
    def reset(self):
        super().reset()
        # self.view.ui.attach(Button("Hello, World!"))
        self.view.ui.attach(
            Button(
                "Hello, World!",
                layout=LayoutBuilder().width(200).height(50).build(),
            )
        )

    def draw(self, renderer: Renderer):
        super().draw(renderer)


def main():
    ButtonTrial().run()


if __name__ == "__main__":
    main()
