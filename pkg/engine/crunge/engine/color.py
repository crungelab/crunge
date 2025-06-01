from enum import Enum
import glm


class Color(Enum):
    RED = (1.0, 0.0, 0.0, 1.0)  # Red with full opacity
    GREEN = (0.0, 1.0, 0.0, 1.0)  # Green with full opacity
    BLUE = (0.0, 0.0, 1.0, 1.0)  # Blue with full opacity
    WHITE = (1.0, 1.0, 1.0, 1.0)  # White with full opacity
    BLACK = (0.0, 0.0, 0.0, 1.0)  # Black with full opacity
    TRANSPARENT = (0.0, 0.0, 0.0, 0.0)  # Fully transparent

    # More colors
    YELLOW = (1.0, 1.0, 0.0, 1.0)  # Yellow
    CYAN = (0.0, 1.0, 1.0, 1.0)  # Cyan
    MAGENTA = (1.0, 0.0, 1.0, 1.0)  # Magenta
    ORANGE = (1.0, 0.5, 0.0, 1.0)  # Orange
    PURPLE = (0.5, 0.0, 0.5, 1.0)  # Purple
    PINK = (1.0, 0.75, 0.8, 1.0)  # Pink
    GRAY = (0.5, 0.5, 0.5, 1.0)  # Gray
    BROWN = (0.65, 0.16, 0.16, 1.0)  # Brown
    GOLD = (1.0, 0.84, 0.0, 1.0)  # Gold
    SILVER = (0.75, 0.75, 0.75, 1.0)  # Silver


def rgba_tuple_to_argb_int(rgba):
    r, g, b, a = [int(round(x * 255.0)) for x in rgba]
    return (a << 24) | (r << 16) | (g << 8) | b
