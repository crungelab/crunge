from typing import TYPE_CHECKING

from loguru import logger
import glm

from ..renderer import Renderer
from ..math import Bounds3
from ..vu import Vu

if TYPE_CHECKING:
    from .renderer.renderer_3d import Renderer3D

from .node_3d import Node3D


class Vu3D(Vu[Node3D]):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self.bounds = Bounds3()

    @property
    def current_renderer(self) -> "Renderer3D":
        return Renderer.get_current()

    @property
    def transform(self) -> glm.mat4:
        return self._transform

    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_transform(self):
        """Self-notification, fired by the transform setter. Subclasses
        that own GPU state mark dirt here."""

    @property
    def size(self) -> glm.vec3:
        raise NotImplementedError

    # -- signals -----------------------------------------------------------
    #
    # Was `on_node_transform_change`, which the base class stopped calling
    # when the handler names moved to the signal_name/on_signal_name
    # convention. Nothing raised — the override was simply orphaned, the
    # transform stayed identity, and everything drew collapsed at the origin.

    def on_transform_changed(self, node: Node3D) -> None:
        self.transform = node.global_transform

    def on_model_changed(self, node: Node3D) -> None:
        pass