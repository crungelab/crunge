import math

from loguru import logger
import glm

from crunge import yoga

from crunge.engine import Widget
from crunge.engine.renderer import Renderer
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.control import Control2D
from crunge.engine.viewport import Viewport
from crunge.engine.easel import OffscreenEasel
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.resource.texture import SpriteTexture
from crunge.engine.d2.settings_2d import Settings2D

from crunge.core.dispatch import DispatchResult, EVENT_UNHANDLED


class WidgetControl2D(Control2D):
    """A scene node that owns a widget tree, renders it into an offscreen easel,
    and presents the result as an ordinary textured quad in the scene.

    The node knows about transform, bounds, sort order and the coordinate hop.
    Everything about *being UI* is delegated to the widget.

    Two sizes are kept apart:

    - logical size: the widget's layout size in pixels. Layout, hit-testing and
      the node's world size are all in these units and never change with zoom.
    - raster size: the texture's pixel dimensions, logical size times the
      raster scale. Only painting knows about it.
    """

    vu_class = SpriteVu

    # Raster scale snaps to powers of two within these limits.
    min_raster_scale = 0.25
    max_raster_scale = 8.0

    # Largest texture dimension allocated, regardless of zoom.
    max_raster_extent = 4096

    # Hysteresis: rescale up as soon as the texture is undersampled (it goes
    # soft), but only rescale down once it's this far oversampled (merely
    # wasteful). Stops rebuilds thrashing when zoom hovers near a power of two.
    upscale_tolerance = 1.01
    downscale_ratio = 2.5

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

    # -- lifecycle ---------------------------------------------------------

    def _create(self):
        super()._create()
        self.ppu = Settings2D().ppu

        self.widget.layout.calculate()
        self.widget.layout.apply()

        # The surface is built lazily on first draw: the widget's size isn't
        # real until layout has run, and the raster scale needs a camera.
        self.easel: OffscreenEasel | None = None
        self.viewport: Viewport | None = None
        self.renderer: Renderer | None = None
        self.texture: SpriteTexture | None = None

        self.raster_scale = 1.0
        self.surface_logical_size = glm.ivec2(0, 0)
        self.surface_dirty = True
        self._warned_zero_size = False

    def _enable(self):
        super()._enable()
        self.layer.add_control(self)
        self.widget.enable()
        # Set before the first draw so culling and sorting see real bounds.
        self.size = glm.vec2(self.logical_size) / self.ppu

    def _disable(self):
        super()._disable()
        self.layer.remove_control(self)
        self.widget.disable()

    def _destroy(self):
        self._release_surface()
        super()._destroy()

    # -- frame -------------------------------------------------------------

    def _update(self, delta_time):
        self.widget.layout.calculate()
        self.widget.layout.apply()
        self.widget.update(delta_time)

        # TODO: gate on a widget dirty flag (hover, press, text change) once
        # widgets have one. Until then every control repaints every frame.
        self.surface_dirty = True

        super()._update(delta_time)

    def _draw(self):
        self.render_surface()
        super()._draw()

    # -- sizes -------------------------------------------------------------

    @property
    def logical_size(self) -> glm.ivec2:
        return glm.ivec2(int(self.widget.width), int(self.widget.height))

    @property
    def raster_size(self) -> glm.ivec2:
        return glm.ivec2(glm.ceil(glm.vec2(self.logical_size) * self.raster_scale))

    # -- raster scale ------------------------------------------------------

    def _screen_scale(self) -> float | None:
        """Screen pixels per logical pixel, as this node currently appears, or
        None if there's no usable camera to measure against.

        Measured by projecting one logical pixel along each local axis, so it
        folds in node scale, parent scale and camera zoom without depending on
        how any of them are represented. Rotation doesn't change a length.

        Must be called outside the offscreen renderer's scope: inside it, the
        current renderer is ours and has no camera.
        """
        renderer = Renderer2D.get_current()
        camera = renderer.camera_2d if renderer is not None else None
        if camera is None:
            return None

        frustum = camera.frustum
        if frustum is None or frustum.width <= 0 or frustum.height <= 0:
            return None

        step = 1.0 / self.ppu
        m = self.global_transform
        origin = glm.vec2(m * glm.vec4(0.0, 0.0, 0.0, 1.0))
        x_axis = glm.vec2(m * glm.vec4(step, 0.0, 0.0, 1.0))
        y_axis = glm.vec2(m * glm.vec4(0.0, step, 0.0, 1.0))

        screen_origin = camera.project(origin)
        sx = glm.length(camera.project(x_axis) - screen_origin)
        sy = glm.length(camera.project(y_axis) - screen_origin)

        # Non-uniform scale: rasterize for the sharper axis.
        return max(sx, sy)

    def _target_raster_scale(self, screen_scale: float, logical: glm.ivec2) -> float:
        """Snap up to the next power of two, so the texture is never
        undersampled, then clamp to the limits."""
        s = max(screen_scale, self.min_raster_scale)
        target = min(2.0 ** math.ceil(math.log2(s)), self.max_raster_scale)

        extent = max(logical.x, logical.y)
        while target > self.min_raster_scale and extent * target > self.max_raster_extent:
            target *= 0.5

        return target

    def _needs_rescale(self, screen_scale: float) -> bool:
        return (
            screen_scale > self.raster_scale * self.upscale_tolerance
            or screen_scale < self.raster_scale / self.downscale_ratio
        )

    def _pending_raster_scale(self, logical: glm.ivec2) -> float | None:
        """The raster scale to rebuild at, or None if the surface is fine."""
        screen_scale = self._screen_scale()

        # No surface yet, or the widget resized: must build. With no camera to
        # measure against, fall back to the current scale.
        if self.easel is None or logical != self.surface_logical_size:
            if screen_scale is None:
                return self.raster_scale
            return self._target_raster_scale(screen_scale, logical)

        # Can't measure, or within tolerance: keep what we have.
        if screen_scale is None or not self._needs_rescale(screen_scale):
            return None

        # Clamping can make the target equal the current scale — e.g. at the
        # maximum while still zooming in. Don't rebuild for nothing.
        target = self._target_raster_scale(screen_scale, logical)
        return target if target != self.raster_scale else None

    # -- surface -----------------------------------------------------------

    def render_surface(self):
        """Keep the texture at on-screen resolution, and repaint it if dirty."""
        logical = self.logical_size
        if logical.x <= 0 or logical.y <= 0:
            if not self._warned_zero_size:
                logger.warning("Widget laid out to zero size; nothing to render")
                self._warned_zero_size = True
            return
        self._warned_zero_size = False

        target = self._pending_raster_scale(logical)
        if target is not None:
            self._build_surface(target, logical)

        if self.surface_dirty:
            self._paint()

    def _build_surface(self, raster_scale: float, logical: glm.ivec2):
        """(Re)create the easel at the given raster scale, and the sprite that
        presents it. The sprite's world size comes from logical size, so a
        rebuild changes sharpness, never how big the control is in the world."""
        self._release_surface()

        self.raster_scale = raster_scale
        raster = self.raster_size

        self.easel = OffscreenEasel(raster)
        self.viewport = Viewport(self.easel)
        self.renderer = Renderer(self.viewport)
        self.texture = SpriteTexture(self.easel.color_texture, raster)
        ResourceManager().texture_kit.add(self.texture)

        self.model = Sprite(self.texture)
        self.size = glm.vec2(logical) / self.ppu

        self.surface_logical_size = logical
        self.surface_dirty = True

        logger.debug(
            f"Widget surface built: logical={logical.x}x{logical.y} "
            f"raster={raster.x}x{raster.y} scale={raster_scale}"
        )

    def _release_surface(self):
        if self.easel is None:
            return
        ResourceManager().texture_kit.remove(self.texture)
        self.easel.destroy()
        self.easel = None
        self.viewport = None
        self.renderer = None
        self.texture = None

    def _paint(self):
        with self.renderer.use():
            canvas = self.renderer.canvas
            # Without a clear, anything the widget doesn't cover opaquely —
            # rounded corners, antialiased edges — accumulates across repaints.
            canvas.clear(0x00000000)
            canvas.save()
            canvas.scale(self.raster_scale, self.raster_scale)
            self.widget.draw()
            canvas.restore()

        self.easel.submit_canvas()
        self.surface_dirty = False

    # -- input -------------------------------------------------------------

    def dispatch_2d(self, event: object, point: glm.vec2) -> DispatchResult:
        if not self.visible or self.easel is None:
            return EVENT_UNHANDLED

        surface_point = self._surface_point(point)
        size = self.logical_size
        if not (0 <= surface_point.x < size.x and 0 <= surface_point.y < size.y):
            return EVENT_UNHANDLED

        return self.widget.dispatch_2d(event, surface_point)

    def _surface_point(self, point: glm.vec2) -> glm.vec2:
        """World -> logical widget pixels.

        The inverse transform removes rotation and scale; PPU and half-extents
        move the origin to the top-left corner, and y flips for the canvas.
        Raster scale never appears: widgets hit-test in logical pixels however
        finely they were rasterized.
        """
        local = glm.inverse(self.global_transform) * glm.vec4(point.x, point.y, 0.0, 1.0)
        size = self.logical_size
        return glm.vec2(
            local.x * self.ppu + size.x * 0.5,
            size.y * 0.5 - local.y * self.ppu,
        )