from ...viewport import Viewport


from ..camera_3d import Camera3D
from ..lighting_3d import Lighting3D

from .renderer_3d import Renderer3D
from ..scene_3d import Scene3D

from .phase import OpaquePhase3D, TransmissivePhase3D


class SceneRenderer3D(Renderer3D):
    def __init__(
        self, scene: Scene3D, viewport: Viewport, camera: Camera3D = None, lighting: Lighting3D = None
    ) -> None:
        super().__init__(viewport, camera=camera, lighting=lighting)
        self.scene = scene

    def create_phases(self) -> None:
        self.phases = [
            OpaquePhase3D(self),
            TransmissivePhase3D(self)
        ]

    '''
    def render(self):
        with self.render_pass():
            self.scene.draw()
    '''