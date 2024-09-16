from enum import Enum
import glm


class Color(Enum):
    def __new__(cls, r, g, b, a=1.0):
        obj = object.__new__(cls)
        obj._value_ = glm.vec4(r, g, b, a)
        return obj
    
    def __getattr__(self, name):
        # Delegate attribute access to the underlying glm.vec4
        return getattr(self._value_, name)

    RED = (1.0, 0.0, 0.0, 1.0)         # Red with full opacity
    GREEN = (0.0, 1.0, 0.0, 1.0)       # Green with full opacity
    BLUE = (0.0, 0.0, 1.0, 1.0)        # Blue with full opacity
    WHITE = (1.0, 1.0, 1.0, 1.0)       # White with full opacity
    BLACK = (0.0, 0.0, 0.0, 1.0)       # Black with full opacity
    TRANSPARENT = (0.0, 0.0, 0.0, 0.0) # Fully transparent
    
    # More colors
    YELLOW = (1.0, 1.0, 0.0, 1.0)      # Yellow
    CYAN = (0.0, 1.0, 1.0, 1.0)        # Cyan
    MAGENTA = (1.0, 0.0, 1.0, 1.0)     # Magenta
    ORANGE = (1.0, 0.5, 0.0, 1.0)      # Orange
    PURPLE = (0.5, 0.0, 0.5, 1.0)      # Purple
    PINK = (1.0, 0.75, 0.8, 1.0)       # Pink
    GRAY = (0.5, 0.5, 0.5, 1.0)        # Gray
    BROWN = (0.65, 0.16, 0.16, 1.0)    # Brown
    GOLD = (1.0, 0.84, 0.0, 1.0)       # Gold
    SILVER = (0.75, 0.75, 0.75, 1.0)   # Silver
"""
class Colors(Enum):
    RED = glm.vec4(1.0, 0.0, 0.0, 1.0)          # Red with full opacity
    GREEN = glm.vec4(0.0, 1.0, 0.0, 1.0)        # Green with full opacity
    BLUE = glm.vec4(0.0, 0.0, 1.0, 1.0)         # Blue with full opacity
    WHITE = glm.vec4(1.0, 1.0, 1.0, 1.0)        # White with full opacity
    BLACK = glm.vec4(0.0, 0.0, 0.0, 1.0)        # Black with full opacity
    TRANSPARENT = glm.vec4(0.0, 0.0, 0.0, 0.0)  # Fully transparent
    
    # More colors
    YELLOW = glm.vec4(1.0, 1.0, 0.0, 1.0)       # Yellow
    CYAN = glm.vec4(0.0, 1.0, 1.0, 1.0)         # Cyan
    MAGENTA = glm.vec4(1.0, 0.0, 1.0, 1.0)      # Magenta
    ORANGE = glm.vec4(1.0, 0.5, 0.0, 1.0)       # Orange
    PURPLE = glm.vec4(0.5, 0.0, 0.5, 1.0)       # Purple
    PINK = glm.vec4(1.0, 0.75, 0.8, 1.0)        # Pink
    GRAY = glm.vec4(0.5, 0.5, 0.5, 1.0)         # Gray
    BROWN = glm.vec4(0.65, 0.16, 0.16, 1.0)     # Brown
    GOLD = glm.vec4(1.0, 0.84, 0.0, 1.0)        # Gold
    SILVER = glm.vec4(0.75, 0.75, 0.75, 1.0)    # Silver
    BRONZE = glm.vec4(0.8, 0.5, 0.2, 1.0)       # Bronze
    TEAL = glm.vec4(0.0, 0.5, 0.5, 1.0)         # Teal
    LIME = glm.vec4(0.0, 1.0, 0.0, 1.0)         # Lime
    OLIVE = glm.vec4(0.5, 0.5, 0.0, 1.0)        # Olive
    MAROON = glm.vec4(0.5, 0.0, 0.0, 1.0)       # Maroon
    NAVY = glm.vec4(0.0, 0.0, 0.5, 1.0)         # Navy
    INDIGO = glm.vec4(0.29, 0.0, 0.51, 1.0)     # Indigo
    AQUA = glm.vec4(0.0, 1.0, 1.0, 1.0)         # Aqua
    TURQUOISE = glm.vec4(0.25, 0.88, 0.82, 1.0) # Turquoise
    SKY_BLUE = glm.vec4(0.53, 0.81, 0.98, 1.0)  # Sky Blue
    ROYAL_BLUE = glm.vec4(0.25, 0.41, 0.88, 1.0) # Royal Blue
    SLATE_BLUE = glm.vec4(0.42, 0.35, 0.80, 1.0) # Slate Blue
    STEEL_BLUE = glm.vec4(0.27, 0.51, 0.71, 1.0) # Steel Blue
    POWDER_BLUE = glm.vec4(0.69, 0.88, 0.90, 1.0) # Powder Blue
    LIGHT_BLUE = glm.vec4(0.68, 0.85, 0.90, 1.0) # Light Blue
    LIGHT_SKY_BLUE = glm.vec4(0.53, 0.81, 0.98, 1.0) # Light Sky Blue
    DEEP_SKY_BLUE = glm.vec4(0.00, 0.75, 1.00, 1.0) # Deep Sky Blue
    DODGER_BLUE = glm.vec4(0.12, 0.56, 1.00, 1.0) # Dodger Blue
    CORNFLOWER_BLUE = glm.vec4(0.39, 0.58, 0.93, 1.0) # Cornflower Blue
    MEDIUM_BLUE = glm.vec4(0.00, 0.00, 0.80, 1.0) # Medium Blue
    DARK_BLUE = glm.vec4(0.00, 0.00, 0.55, 1.0) # Dark Blue
    MIDNIGHT_BLUE = glm.vec4(0.10, 0.10, 0.44, 1.0) # Midnight Blue
    DARK_SLATE_BLUE = glm.vec4(0.28, 0.24, 0.55, 1.0) # Dark Slate Blue
    CADET_BLUE = glm.vec4(0.37, 0.62, 0.63, 1.0) # Cadet Blue
    DARK_TURQUOISE = glm.vec4(0.00, 0.81, 0.82, 1.0) # Dark Turquoise
    MEDIUM_TURQUOISE = glm.vec4(0.28, 0.82, 0.80, 1.0) # Medium Turquoise
    PALE_TURQUOISE = glm.vec4(0.69, 0.93, 0.93, 1.0) # Pale Turquoise
    LIGHT_CYAN = glm.vec4(0.88, 1.00, 1.00, 1.0) # Light Cyan
    DARK_CYAN = glm.vec4(0.00, 0.55, 0.55, 1.0) # Dark Cyan
"""