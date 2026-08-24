from dataclasses import dataclass

from glm import ivec2

from crunge.engine.scene.layer.composite_layer import CompositeLayer
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.compositor import Compositor
from crunge.engine.renderer.task.composite_phase import CompositeItem, CompositePhase


@dataclass
class CompositeLayer2DMemo:
    easel: OffscreenEasel
    camera: Camera2D
    renderer: Renderer2D


class CompositeLayer2D(CompositeLayer):
    def __init__(self, name: str):
        super().__init__(name)
        self.compositor = Compositor()
        self._memo: CompositeLayer2DMemo = None

    @property
    def memo(self):
        if self._memo is None:
            current_viewport = Viewport.get_current()
            current_easel = current_viewport.easel
            current_renderer = Renderer2D.get_current()

            easel = OffscreenEasel(
                ivec2(current_viewport.width, current_viewport.height),
                current_easel.render_options,
            )

            camera=Camera2D(leader=current_renderer.camera_2d)
            renderer=Renderer2D(current_viewport, camera=camera, clear=False)

            self._memo = CompositeLayer2DMemo(
                easel=easel,
                camera=camera,
                renderer=renderer
            )
        return self._memo

    def _draw(self):
        current_viewport = Viewport.get_current()
        current_renderer = Renderer2D.get_current()

        def do_composite():
            memo = self.memo
            with memo.easel.frame():
                with memo.renderer.frame(encoder=current_renderer.encoder):
                    memo.renderer.render(self)

            self.compositor.composite(
                current_renderer.encoder,
                src_view=memo.easel.color_texture_view,
                dst_view=current_viewport.easel.color_texture_view,
                is_premultiplied=True
            )

        phase: CompositePhase = current_renderer.plan.get_phase(CompositePhase)
        phase.add(CompositeItem(do_composite))

    def render(self):
        for child in self.children:
            child.draw()
