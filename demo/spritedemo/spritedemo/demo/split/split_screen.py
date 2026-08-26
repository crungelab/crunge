from loguru import logger

from crunge import yoga

from crunge.engine.d2.screen import SceneScreen2D

from .split_view import SplitView

class SplitScreen(SceneScreen2D):
    def create_views(self):
        self.style = yoga.StyleBuilder().size_percent(100, 100).flex_direction(
            yoga.FlexDirection.ROW
        ).build()  # ASSUMPTION: builder method + enum names

        style = yoga.StyleBuilder().size_percent(50, 100).build()
        for i in range(2):
            view = SplitView(self.scene)
            view.style = style
            self.add_child(view)
