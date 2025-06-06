from pathlib import Path

from loguru import logger

from crunge import engine

from .trial_view import TrialView


class Trial(engine.App):
    view: TrialView

    kWidth = 1024
    kHeight = 768

    def __init__(self, view=TrialView()):
        super().__init__(
            self.kWidth,
            self.kHeight,
            self.__class__.__name__,
            view=view,
            resizable=True,
        )
        self.resource_root = (
            Path(__file__).parent.parent.parent.parent.parent / "resources"
        )
