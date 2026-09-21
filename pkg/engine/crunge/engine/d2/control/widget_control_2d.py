from loguru import logger
import glm

from crunge import yoga

from crunge.engine import Widget
from crunge.engine.renderer import Renderer
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.control import Control2D
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.resource.texture import SpriteTexture
from crunge.engine.d2.settings_2d import Settings2D

from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED


class WidgetControl2D(Control2D):
    """A scene node that owns a widget tree, renders it into an offscreen easel,
    and presents the result as an ordinary textured quad in the scene.

    The node knows about transform, bounds, sort order and the coordinate hop.
    Everything about *being UI* is delegated to the widget.
    """
    vu_class = SpriteVu

    def __init__(
        self,
        widget: Widget,
        position: glm.vec2 = None,
        rotation=0.0,
        scale: glm.vec2 = None,
        model: object = None,
        children: list["Control2D"] = None,
        size: glm.vec2 = None,
        style: yoga.Style = None,
    ) -> None:
        # style last, so Node2D's positional order is unchanged for existing
        # call sites. Everything here reads better as keywords anyway.
        super().__init__(position, rotation, scale, model, children, size, style)
        self.widget = widget

    def _create(self):
        super()._create()
        self.ppu = Settings2D().ppu

        self.widget.layout.set_size(100, 50)
        self.widget.layout.calculate()
        self.widget.layout.apply()
        logger.debug("Widget size: {}", self.widget.size)

        # Created lazily: the widget's size isn't real until layout has run.
        self.easel: OffscreenEasel | None = None
        self.viewport: Viewport | None = None
        self.texture: SpriteTexture | None = None
        self.surface_dirty = True


    def _enable(self):
        super()._enable()
        self.layer.add_control(self)
        self.widget.enable()
        logger.debug(f"Widget size: {self.widget.size}, PPU: {self.ppu}")
        self.size = glm.vec2(self.widget.size) / self.ppu

    def _disable(self):
        super()._disable()
        self.layer.remove_control(self)
        self.widget.disable()

    def _destroy(self):
        if self.easel is not None:
            ResourceManager().texture_kit.remove(self.texture)
            self.easel.destroy()
            self.easel = None
            self.viewport = None
            self.texture = None
        super()._destroy()

    # -- surface -----------------------------------------------------------

    @property
    def surface_size(self) -> glm.ivec2:
        return glm.ivec2(int(self.widget.width), int(self.widget.height))

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
            self.widget.layout.calculate()
            self.widget.layout.apply()

            if not self.create_surface():
                logger.warning("Widget laid out to zero size; nothing to render")
                return

        if not self.surface_dirty:
            return

        with self.renderer.use():
            self.widget.draw()

        self.easel.submit_canvas()
        self.surface_dirty = False

    # -- input -------------------------------------------------------------
    def dispatch_2d(self, event: object, point: glm.vec2) -> DispatchResult:
        logger.debug(f"Dispatching event: {event}")

        if not self.visible or self.easel is None:
            return EVENT_UNHANDLED

        logger.debug(f"Widget visible: {self.visible}, easel: {self.easel}")

        # World -> local -> surface pixels. bounds is local space, so the ratio of
        # surface size to bounds size is the conversion, no PPU lookup needed.
        local = glm.inverse(self.global_transform) * glm.vec4(
            point.x, point.y, 0.0, 1.0
        )

        size = self.surface_size
        surface_point = glm.vec2(
            local.x * self.ppu + size.x * 0.5,
            size.y * 0.5 - local.y * self.ppu,
        )

        size = self.surface_size
        if not (0 <= surface_point.x < size.x and 0 <= surface_point.y < size.y):
            return EVENT_UNHANDLED

        return self.widget.dispatch_2d(event, surface_point)

    # -- frame -------------------------------------------------------------
    def _draw(self):
        self.render_surface()
        super()._draw()

    def _update(self, delta_time):
        self.widget.layout.calculate()
        self.widget.layout.apply()

        self.widget.update(delta_time)

        # ASSUMPTION: widgets expose a dirty flag set on hover/press/text change.
        # Without this the offscreen pass runs every frame for every control.
        self.surface_dirty = True
        """
        if self.widget.dirty:
            self.surface_dirty = True
        """
        super()._update(delta_time)
