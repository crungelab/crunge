from typing import TYPE_CHECKING, Generic, TypeVar

from ..node import Node
from ..viewport import Viewport

if TYPE_CHECKING:
    from ..d2.camera_2d import Camera2D
    from ..d3.camera_3d import Camera3D
    from ..d3.lighting_3d import Lighting3D

from .renderer import Renderer
from .task import RenderPlan


T_Renderer = TypeVar("T_Renderer", bound="Renderer")
T_Scene = TypeVar("T_Scene")


class SceneRenderer(Generic[T_Renderer, T_Scene], Renderer):
    def __init__(
        self,
        scene: T_Scene,
        viewport: Viewport,
        camera_2d: "Camera2D" = None,
        camera_3d: "Camera3D" = None,
        lighting_3d: "Lighting3D" = None,
    ) -> None:
        super().__init__(viewport, camera_2d=camera_2d, camera_3d=camera_3d, lighting_3d=lighting_3d)
        self.scene = scene
        self.plan: RenderPlan[T_Renderer] = None

    def create_plan(self) -> None:
        pass

    def ensure_plan(self) -> None:
        if self.plan is None:
            self.create_plan()

    def render(self, node: Node = None) -> None:
        if node is None:
            node = self.scene
        self.ensure_plan()
        with self.frame():
            with self.render_pass():
                node.render()
            self.plan.render()
        self.plan.clear()
