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
