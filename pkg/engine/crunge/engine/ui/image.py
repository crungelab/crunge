from enum import Enum, auto

from loguru import logger
import glm

from crunge import skia
from crunge import yoga

from ..resource.resource_manager import ResourceManager
from ..widget import Widget, WidgetLayout
from ..renderer import Renderer


class ImageFit(Enum):
    """How the image fills the box yoga gave it, when the box and the image
    disagree on shape. Same meanings as CSS object-fit."""

    FILL = auto()  # stretch to the box; aspect ratio not kept
    CONTAIN = auto()  # largest that fits entirely; letterboxed
    COVER = auto()  # smallest that covers the box; overflow clipped
    NONE = auto()  # natural size, centered; overflow clipped


class ImageLayout(WidgetLayout):
    """A widget layout that asks its node for an intrinsic size."""

    @property
    def measurable(self) -> bool:
        return True


class Image(Widget):
    """A bitmap that sizes itself like an <img>.

    With no style size it lays out at its natural pixel size. Give it one
    dimension -- height(50) for an icon row -- and yoga derives the other from
    the aspect ratio. Give it both and the box is fixed, and `fit` decides how
    the image sits inside it.

    The aspect ratio goes to yoga as a style property rather than being worked
    out in on_measure, for the same reason Control2D gives: in the style, the
    flex algorithm can see it; computed in measure, it's invisible to flex.

    Decoded images are cached by resolved path for the life of the process.
    A Dash drawer of icon buttons will load the same few files many times, and
    decoding is the expensive part.
    """

    layout_class = ImageLayout

    _cache: dict[str, skia.Image] = {}

    def __init__(
        self,
        src: str,
        fit: ImageFit = ImageFit.CONTAIN,
        keep_aspect: bool = True,
        style: yoga.Style = None,
        **kwargs,
    ):
        super().__init__(style=style, **kwargs)
        self.fit = fit
        self.keep_aspect = keep_aspect
        self.sampling = skia.SamplingOptions(skia.FilterMode.K_LINEAR)  # ASSUMPTION: binding names

        self._src: str | None = None
        self.image: skia.Image | None = None
        self.src = src

    # -- source ------------------------------------------------------------

    @property
    def src(self) -> str | None:
        return self._src

    @src.setter
    def src(self, value: str) -> None:
        if value == self._src:
            return
        self._src = value
        self.image = self._load(value)
        self._apply_aspect_ratio()
        # The intrinsic size changed, so yoga's cached measurement is stale.
        # ASSUMPTION: binding names YGNodeMarkDirty mark_dirty
        self.layout.layout_node.mark_dirty()

    @classmethod
    def _load(cls, src: str) -> skia.Image | None:
        path = str(ResourceManager().resolve_path(src))

        cached = cls._cache.get(path)
        if cached is not None:
            return cached

        data = skia.Data.make_from_file_name(path)
        if data is None or data.size() == 0:
            logger.warning(f"Image: could not read {src!r} ({path})")
            return None

        image = skia.deferred_from_encoded_data(data)
        if image is None:
            logger.warning(f"Image: could not decode {src!r} ({path})")
            return None

        cls._cache[path] = image
        return image

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()

    @property
    def natural_size(self) -> glm.vec2:
        if self.image is None:
            return glm.vec2(0.0, 0.0)
        return glm.vec2(self.image.width(), self.image.height())

    def _apply_aspect_ratio(self) -> None:
        natural = self.natural_size
        if not self.keep_aspect or natural.x <= 0 or natural.y <= 0:
            return
        # Width over height, yoga's convention. Ignored by yoga when the style
        # fixes both dimensions, which is what `fit` is for.
        # ASSUMPTION: binding names YGNodeStyleSetAspectRatio set_aspect_ratio
        self.layout.layout_node.set_aspect_ratio(natural.x / natural.y)

    # -- layout ------------------------------------------------------------

    def on_measure(
        self, width: float, width_mode: str, height: float, height_mode: str
    ) -> glm.vec2:
        """Natural pixel size, within yoga's constraints.

        Pure: yoga calls this several times per pass while flex resolves. Each
        axis is clamped independently; keeping the proportions is the aspect
        ratio style's job, not this function's.
        """
        natural = self.natural_size
        return glm.vec2(
            self._measure_axis(natural.x, width, width_mode),
            self._measure_axis(natural.y, height, height_mode),
        )

    @staticmethod
    def _measure_axis(natural: float, available: float, mode: str) -> float:
        if mode == "exactly":
            return available
        if mode == "at_most":
            return min(natural, available)
        return natural

    # -- draw --------------------------------------------------------------

    def _dest_rect(self, box_pos: glm.vec2, box_size: glm.vec2) -> tuple[glm.vec2, glm.vec2]:
        """Where the image lands for the current fit: position and size."""
        natural = self.natural_size

        if self.fit is ImageFit.FILL:
            return box_pos, box_size

        if self.fit is ImageFit.NONE:
            scale = 1.0
        else:
            sx = box_size.x / natural.x
            sy = box_size.y / natural.y
            scale = min(sx, sy) if self.fit is ImageFit.CONTAIN else max(sx, sy)

        size = natural * scale
        return box_pos + (box_size - size) * 0.5, size

    def _draw(self):
        natural = self.natural_size
        box_size = glm.vec2(self.size)
        if self.image is None or natural.x <= 0 or natural.y <= 0:
            super()._draw()
            return
        if box_size.x <= 0 or box_size.y <= 0:
            super()._draw()
            return

        canvas = Renderer.get_current().canvas
        box_pos = glm.vec2(self.global_position)
        pos, size = self._dest_rect(box_pos, box_size)

        # COVER and NONE can overflow the box; everything else fits inside it.
        clip = self.fit in (ImageFit.COVER, ImageFit.NONE)
        if clip:
            canvas.save()
            canvas.clip_rect(_rect(box_pos, box_size))

        # ASSUMPTION: binding mirrors drawImageRect(image, dst, sampling)
        canvas.draw_image_rect(self.image, _rect(pos, size), self.sampling)

        if clip:
            canvas.restore()

        super()._draw()


def _rect(pos: glm.vec2, size: glm.vec2) -> skia.Rect:
    # ASSUMPTION: skia.Rect takes left, top, right, bottom
    return skia.Rect(pos.x, pos.y, size.x, size.y)