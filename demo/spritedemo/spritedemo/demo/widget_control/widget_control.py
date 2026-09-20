import dataclasses
from loguru import logger
import glm

from crunge import imgui
from crunge.yoga import StyleBuilder

from crunge.engine.renderer import Renderer
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine import colors, compose
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.resource.texture import SpriteTexture
from crunge.engine.ui.button import Button
from crunge.engine.d2.settings_2d import Settings2D

from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED

from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01


class WidgetControl(Node2D):
    """A scene node that owns a widget tree, renders it into an offscreen easel,
    and presents the result as an ordinary textured quad in the scene.

    The node knows about transform, bounds, sort order and the coordinate hop.
    Everything about *being UI* is delegated to the widget.
    """

    def _create(self):
        super()._create()
        self.ppu = Settings2D().ppu
        #self.button = Button("Click Me")
        self.button = Button(
            "Hello, World!",
            on_click=self.on_click,
            style=StyleBuilder().size(200, 50).build(),
        )

        self.button.layout.set_size(100, 50)
        self.button.layout.calculate()
        self.button.layout.apply()
        logger.debug("Button size: {}", self.button.size)

        # Created lazily: the widget's size isn't real until layout has run.
        self.easel: OffscreenEasel | None = None
        self.viewport: Viewport | None = None
        self.texture: SpriteTexture | None = None
        self.surface_dirty = True

    def on_click(self):
        logger.debug("Button clicked")

    def _enable(self):
        super()._enable()
        self.layer.add_control(self)
        self.button.enable()
        logger.info(f"Button size: {self.button.size}, PPU: {self.ppu}")
        self.size = glm.vec2(self.button.size) / self.ppu

    def _disable(self):
        super()._disable()
        self.layer.remove_control(self)
        self.button.disable()

    def _destroy(self):
        if self.easel is not None:
            # ASSUMPTION: texture_kit.remove() takes the texture object
            ResourceManager().texture_kit.remove(self.texture)
            # ASSUMPTION: OffscreenEasel exposes destroy()
            self.easel.destroy()
            self.easel = None
            self.viewport = None
            self.texture = None
        super()._destroy()

    # -- surface -----------------------------------------------------------

    @property
    def surface_size(self) -> glm.ivec2:
        # ASSUMPTION: Button exposes its computed layout size as .width / .height
        return glm.ivec2(int(self.button.width), int(self.button.height))

    def create_surface(self) -> bool:
        """Build the easel and the sprite that presents it. Returns False if the
        widget still has no size, so the caller can try again next frame."""
        size = self.surface_size
        if size.x <= 0 or size.y <= 0:
            return False

        self.easel = OffscreenEasel(size)
        self.viewport = Viewport(self.easel)
        self.renderer = Renderer(self.viewport)
        self.texture = SpriteTexture(self.easel.color_texture, size)
        ResourceManager().texture_kit.add(self.texture)

        self.model = Sprite(self.texture)

        logger.debug(f"Widget surface created at {size.x}x{size.y}")
        return True

    def render_surface(self):
        """Paint the widget into its own easel. Must run *outside* the frame's
        compose scope — call it before the scene draws, not from _draw()."""
        if self.easel is None:
            # ASSUMPTION: layout() runs the yoga pass for a rootless widget.
            # If a widget needs a root to be measured, give it a Panel parent here.
            self.button.layout.calculate()
            self.button.layout.apply()

            if not self.create_surface():
                logger.warning("Widget laid out to zero size; nothing to render")
                return

        if not self.surface_dirty:
            return

        with self.renderer.use():
            self.button.draw()

        self.easel.submit_canvas()
        self.surface_dirty = False

    # -- input -------------------------------------------------------------
    def dispatch_2d(self, event: object, point: glm.vec2):
        logger.debug(f"Dispatching event: {event}")

        if not self.visible or self.easel is None:
            return False

        logger.debug(f"Widget visible: {self.visible}, easel: {self.easel}")


        # World -> local -> surface pixels. bounds is local space, so the ratio of
        # surface size to bounds size is the conversion, no PPU lookup needed.
        local = glm.inverse(self.global_transform) * glm.vec4(point.x, point.y, 0.0, 1.0)
        # ASSUMPTION: bounds exposes .min and .size as vec2
        scale = glm.vec2(self.surface_size) / self.global_bounds.size
        surface_point = (glm.vec2(local.x, local.y) - self.global_bounds.min) * scale

        size = self.surface_size
        if not (0 <= surface_point.x < size.x and 0 <= surface_point.y < size.y):
            return False

        return self.button.dispatch_2d(event, surface_point)

    '''
    def dispatch(self, event: object):
        logger.debug(f"Dispatching event: {event}")

        if not self.visible or self.easel is None:
            return False

        logger.debug(f"Widget visible: {self.visible}, easel: {self.easel}")

        # ASSUMPTION: positional events carry .position in world space
        point = getattr(event, "position", None)
        if point is None:
            return self.button.dispatch(event)

        # World -> local -> surface pixels. bounds is local space, so the ratio of
        # surface size to bounds size is the conversion, no PPU lookup needed.
        local = glm.inverse(self.global_transform) * glm.vec4(point.x, point.y, 0.0, 1.0)
        # ASSUMPTION: bounds exposes .min and .size as vec2
        scale = glm.vec2(self.surface_size) / self.global_bounds.size
        surface_point = (glm.vec2(local.x, local.y) - self.global_bounds.min) * scale

        size = self.surface_size
        if not (0 <= surface_point.x < size.x and 0 <= surface_point.y < size.y):
            return False

        # ASSUMPTION: the widget tree can be dispatched at an explicit local point
        #return self.button.dispatch(surface_point, event)
        return self.button.dispatch(event)
        '''
    # -- frame -------------------------------------------------------------

    def _update(self, delta_time):
        self.button.layout.calculate()
        self.button.layout.apply()

        self.button.update(delta_time)

        # ASSUMPTION: widgets expose a dirty flag set on hover/press/text change.
        # Without this the offscreen pass runs every frame for every control.
        self.surface_dirty = True
        '''
        if self.button.dirty:
            self.surface_dirty = True
        '''
        super()._update(delta_time)


class WidgetControlDemo(Demo):
    def setup(self):
        super().setup()

        self.rotation = 0
        self.scale = 1.0

        self.node = WidgetControl().seat(SpriteVu())
        self.scene.attach(self.node)

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None

    def _draw(self):
        # Offscreen work first, in its own compose scope, before the scene draws.
        if self.node is not None:
            self.node.render_surface()

        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Widget Control")

        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        if changed and self.node is not None:
            self.node.rotation = self.rotation

        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        if changed and self.node is not None:
            self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        # TODO: camera zoom slider here once the surface renders — zoom is the
        # rasterization-scale test and the reason this demo exists.

        super()._draw()


def main():
    WidgetControlDemo().run()


if __name__ == "__main__":
    main()