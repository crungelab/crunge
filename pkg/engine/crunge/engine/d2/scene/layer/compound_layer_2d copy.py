from dataclasses import dataclass

from glm import ivec2

from crunge.engine.scene.layer.compound_layer import CompoundLayer
from crunge.engine.viewport import Viewport
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.renderer.task.composite_phase import CompositeItem, CompositePhase


@dataclass
class CompoundLayer2DMemo:
    camera: Camera2D
    renderer: Renderer2D


class CompoundLayer2D(CompoundLayer):
    def __init__(self, name: str):
        super().__init__(name)
        self._memo: CompoundLayer2DMemo = None
        # self.camera = Camera2D()
        #current_viewport = Viewport.get_current()
        #self.renderer = Renderer2D(current_viewport, camera=self.camera, clear=False)

    @property
    def memo(self):
        current_viewport = Viewport.get_current()
        current_renderer = Renderer2D.get_current()
        if self._memo is None:
            camera=Camera2D(leader=current_renderer.camera_2d)
            renderer=Renderer2D(current_viewport, camera=camera, clear=False)

            self._memo = CompoundLayer2DMemo(
                camera=camera,
                renderer=renderer
            )
        return self._memo

    def _render(self):
        current_renderer = Renderer2D.get_current()

        # self.camera.position = current_renderer.camera_2d.position
        # self.camera.zoom = current_renderer.camera_2d.zoom

        def do_render():
            renderer = self.memo.renderer
            with renderer.frame(encoder=current_renderer.encoder):
                renderer.render(self)

        phase: CompositePhase = current_renderer.plan.get_phase(CompositePhase)
        phase.add(CompositeItem(do_render))

    def root_render(self):
        for child in self.children:
            child.render()
