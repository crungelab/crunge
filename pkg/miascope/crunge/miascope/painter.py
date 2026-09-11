"""Draws a Scene on a Skia canvas.

Every crunge.skia call lives in this file and is marked `# ASSUMPTION` where I
haven't seen the binding. `check_bindings.py` lists them with dir()-style
checks, so any mismatch should be a one-line fix here.
"""

from __future__ import annotations

from crunge import skia

from .camera import Camera
from .model import Node
from .scene import Scene
from .style import EDGE, FONT_SIZE, MIN_TEXT_PIXELS, PHASE_FILL, SELECTED, SOLUTION_EDGE, SPAWN_EDGE, TEXT


def make_font(size: float):
    # ASSUMPTION: skia.Font() and Font.set_size(). Recent Skia has no implicit
    # default typeface; if labels draw nothing, get a typeface from the font
    # manager crunge.skia exposes and pass it to the Font constructor.
    font = skia.Font()
    font.set_size(size)
    return font


def make_paint(color, stroke: bool = False, width: float = 1.0):
    paint = skia.Paint()
    paint.set_anti_alias(True)            # ASSUMPTION
    paint.set_color4f(skia.Color4f(*color))  # ASSUMPTION: color space argument optional
    if stroke:
        paint.set_stroke(True)            # ASSUMPTION: SkPaint::setStroke(bool)
        paint.set_stroke_width(width)     # ASSUMPTION
    return paint


class Painter:
    def __init__(self, font_size: float = FONT_SIZE):
        self.font_size = font_size
        self.font = make_font(font_size)
        self.text = make_paint(TEXT)
        self.fills = {phase: make_paint(color) for phase, color in PHASE_FILL.items()}
        self.edge = make_paint(EDGE, stroke=True, width=1.5)
        self.spawn_edge = make_paint(SPAWN_EDGE, stroke=True, width=2.0)
        self.solution_edge = make_paint(SOLUTION_EDGE, stroke=True, width=3.0)
        self.selected = make_paint(SELECTED, stroke=True, width=3.0)

    def measure(self, text: str) -> float:
        # SkFont::measureText takes (const void*, size_t, SkTextEncoding, SkRect*),
        # which needs a hand-written binding. Until it exists, estimate the width.
        if hasattr(self.font, "measure_text"):
            return self.font.measure_text(text)
        return 0.6 * self.font_size * len(text)

    def paint(self, canvas, scene: Scene, camera: Camera, t: int | None,
              selected: Node | None, width: float, height: float) -> None:
        rect = camera.visible(width, height)
        canvas.save()                                   # ASSUMPTION
        canvas.scale(camera.zoom, camera.zoom)          # ASSUMPTION
        canvas.translate(-camera.x, -camera.y)          # ASSUMPTION

        for edge in scene.visible_edges(t, rect):
            paint = self.solution_edge if edge.solution else self.spawn_edge if edge.spawn else self.edge
            canvas.draw_line(edge.x0, edge.y0, edge.x1, edge.y1, paint)   # ASSUMPTION

        radius = scene.padding
        baseline = scene.padding + scene.font_size * 0.8
        readable = scene.font_size * camera.zoom >= MIN_TEXT_PIXELS
        for box, phase in scene.visible(t, rect):
            r = skia.Rect(box.left, box.top, box.right - box.left, box.bottom - box.top)
            canvas.draw_round_rect(r, radius, radius, self.fills[phase])   # ASSUMPTION
            if box.node is selected:
                canvas.draw_round_rect(r, radius, radius, self.selected)
            if readable:
                canvas.draw_string(box.node.label, box.left + scene.padding, box.top + baseline,
                                   self.font, self.text)      # ASSUMPTION

        canvas.restore()
