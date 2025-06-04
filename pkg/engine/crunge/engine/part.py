from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .widget import Widget

class Part:
    def __init__(self):
        self.widget: "Widget" = None