from glm import ivec2

from crunge.engine.scene.layer.compound_layer import CompoundLayer
from crunge.engine.viewport import Viewport
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.renderer.task.composite_phase import CompositeItem, CompositePhase

    
class CompoundLayer2D(CompoundLayer):
    def __init__(self, name: str):
        super().__init__(name)
        self.camera = Camera2D()
        current_viewport = Viewport.get_current()
        self.renderer = Renderer2D(current_viewport, camera=self.camera, clear=False)

    def _render(self):
        current_renderer = Renderer2D.get_current()

        self.camera.position = current_renderer.camera_2d.position
        self.camera.zoom = current_renderer.camera_2d.zoom

        def do_render():
            with self.renderer.frame(encoder=current_renderer.encoder):
                self.renderer.render(self)

        phase: CompositePhase = current_renderer.plan.get_phase(CompositePhase)
        phase.add(CompositeItem(do_render))

    def root_render(self):
        for child in self.children:
            child.render()
