import glm

RESERVED_BINDINGS = 2
TEXTURE_BINDING_START = RESERVED_BINDINGS

RESERVED_LOCATIONS = 1
LOCATION_START = RESERVED_LOCATIONS + 1

WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)
WORLD_SCALE = 1

# Debug
DEBUG_COLLISION = False

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

# Default mass used for sprites
DEFAULT_MASS = 1

GRAVITY = (0.0, -981.0)

# Physics Types

PT_STATIC = 0
PT_KINEMATIC = 1
PT_DYNAMIC = 2
PT_GROUP = 3

# Geom Types

GT_GROUP = 0
GT_BOX = 1
GT_BALL = 2
GT_HULL = 3
GT_DECOMPOSED = 4

# Grid-size
SPRITE_SIZE = 128

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = 100

# Constants used to scale our sprites from their original size
SPRITE_SCALING = 0.5
CHARACTER_SCALING = 1

TILE_WIDTH = 128
TILE_SCALING = 1
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
