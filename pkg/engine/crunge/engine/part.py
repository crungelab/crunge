from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pane import Pane

class Part:
    def __init__(self):
        self.widget: "Pane" = None