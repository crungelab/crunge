from crunge.core.chip import Chip
from typing import TYPE_CHECKING
from .cursors import CURSOR_HAND

if TYPE_CHECKING:
    from .widget import Widget

class CursorChip(Chip["Widget"]):
    def __init__(self, cursor=CURSOR_HAND) -> None:
        super().__init__()
        self.cursor = cursor