"""Colors and sizes for drawing traces. Colors are RGBA floats, like crunge.engine.colors."""

from .model import Phase

FONT_SIZE = 11.0
PADDING = 3.0   # inside a node box, around its label
GAP = 10.0      # between neighboring boxes on a level
LEVEL = 34.0    # between the tops of successive levels
MIN_TEXT_PIXELS = 5.0  # labels smaller than this on screen aren't drawn

PHASE_FILL = {
    Phase.RUNNING: (0.50, 0.50, 0.55, 1.0),
    Phase.QUEUED: (0.25, 0.50, 0.85, 1.0),
    Phase.EXPANDED: (0.32, 0.36, 0.45, 1.0),
    Phase.PRUNED: (0.50, 0.40, 0.20, 1.0),
    Phase.SKIPPED: (0.42, 0.32, 0.32, 1.0),
    Phase.DEAD: (0.62, 0.20, 0.20, 1.0),
    Phase.SOLUTION: (0.18, 0.62, 0.32, 1.0),
}

TEXT = (0.95, 0.95, 0.95, 1.0)
EDGE = (0.55, 0.57, 0.62, 1.0)
SPAWN_EDGE = (0.75, 0.55, 0.90, 1.0)
SOLUTION_EDGE = (0.35, 0.85, 0.45, 1.0)
SELECTED = (1.00, 0.85, 0.20, 1.0)

CHANGE_TEXT = {
    "added": (0.45, 0.90, 0.50, 1.0),
    "removed": (0.95, 0.45, 0.45, 1.0),
    "kept": (0.85, 0.85, 0.85, 1.0),
}
ERROR_TEXT = (0.95, 0.45, 0.45, 1.0)
