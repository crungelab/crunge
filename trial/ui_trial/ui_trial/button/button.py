from loguru import logger

from crunge.engine import Renderer
from crunge.engine.widget.button import Button
from crunge.yoga import StyleBuilder

from ..trial import Trial


class ButtonTrial(Trial):
    def setup(self):
        super().setup()
        self.view.ui.add_child(
            Button(
                "Hello, World!",
                style=StyleBuilder().size(200, 50).build(),
            )
        )


def main():
    ButtonTrial().run()


if __name__ == "__main__":
    main()
