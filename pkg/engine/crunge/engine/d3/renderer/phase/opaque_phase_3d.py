from .render_phase_3d import RenderPhase3D


class OpaquePhase3D(RenderPhase3D):
    def render(self) -> None:
        with self.renderer.render_pass():
            self.renderer.scene.draw()

#TODO: Not there yet
'''
from .item_phase_3d import ItemPhase3D


class OpaquePhase3D(ItemPhase3D):
    def render(self) -> None:
        with self.renderer.render_pass():
            self.renderer.scene.draw()
'''