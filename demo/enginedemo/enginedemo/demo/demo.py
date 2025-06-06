from pathlib import Path

from crunge import engine

from .demo_view import DemoView

class Demo(engine.App):
    def __init__(self, view=DemoView()):
        super().__init__(
            title=self.__class__.__name__,
            view=view,
            resizable=True,
        )
        self.resource_root = Path(__file__).parent.parent.parent.parent.parent / "resources"
