from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass

from ...vu import Vu

if TYPE_CHECKING:
    from ..renderer import Renderer

DrawCallback = Callable[["Renderer"], None]


@dataclass(slots=True)
class FilterItem:
    vu: Vu
    callback: DrawCallback
