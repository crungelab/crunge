from typing import Any, Generic, TypeVar

import glm

from ..vu_group import VuGroup
from .vu_2d import Vu2D

T_Vu = TypeVar("T_Vu", bound=Vu2D)


class VuGroup2D(VuGroup[T_Vu], Generic[T_Vu]):
    pass