import glm

from crunge import skia

from .. import Widget
from ..widget import WidgetLayout
from ..renderer import Renderer


class TextLayout(WidgetLayout):
    """A widget layout that asks its node for an intrinsic size."""

    measurable = True


class Text(Widget):
    """A single line of text that sizes itself to its content.

    Give it no width or height in its style and yoga will ask on_measure
    instead. An explicit size in the style still wins -- yoga skips the
    measure call for a dimension it already knows exactly.
    """

    layout_class = TextLayout

    def __init__(self, text: str = "", font_size: float = 36, **kwargs):
        super().__init__(**kwargs)
        # Plain fields here, not the setters: the setters dirty the
        # layout, and nothing has been measured yet to be stale.
        self._text = text
        self.paint = skia.Paint()
        self.paint.set_color(0xFFFF00FF)
        self.font = skia.Font()
        self.font.set_size(font_size)

    # -- content -----------------------------------------------------------
    #
    # Anything that changes the measured size goes through a setter that
    # calls remeasure. Assigning to self.font directly, or calling
    # font.set_size, changes the size without telling yoga.

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if value == self._text:
            return
        self._text = value
        self.layout.remeasure()

    @property
    def font_size(self) -> float:
        return self.font.get_size()

    @font_size.setter
    def font_size(self, value: float) -> None:
        self.font.set_size(value)
        self.layout.remeasure()

    # -- measurement -------------------------------------------------------

    def on_measure(
        self, width: float, width_mode: str, height: float, height_mode: str
    ) -> glm.vec2:
        """Intrinsic size of the text, within yoga's constraints.

        Pure: yoga calls this several times per pass while flex resolves.
        Single-line, so the available width never changes the height.
        Wrapping would be the reason to use it.
        """
        # ASSUMPTION: binding names. SkFont::measureText and
        # SkFont::getMetrics; the metric fields may come through as
        # fAscent/fDescent depending on how cxbind named them.
        metrics = self.font.get_metrics()
        measured_width = self.font.measure_text(self._text)
        # Skia's ascent is negative (above the baseline), so this is the
        # full box from the top of the tallest glyph to the lowest descender.
        measured_height = metrics.descent - metrics.ascent

        return glm.vec2(
            self._constrain(measured_width, width, width_mode),
            self._constrain(measured_height, height, height_mode),
        )

    @staticmethod
    def _constrain(measured: float, available: float, mode: str) -> float:
        if mode == "exactly":
            return available
        if mode == "at_most":
            return min(measured, available)
        return measured  # "undefined": available is nan, size to content

    # -- drawing -----------------------------------------------------------

    def _draw(self):
        canvas = Renderer.get_current().canvas
        position = self.global_position
        metrics = self.font.get_metrics()
        # draw_string takes a baseline, not a top edge. The box on_measure
        # reported starts at the ascent, so the baseline sits -ascent
        # below the top of the box.
        canvas.draw_string(
            self._text,
            position.x,
            position.y - metrics.ascent,
            self.font,
            self.paint,
        )