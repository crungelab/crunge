from .geom import Geom, BoxGeom, BallGeom
from .physics import Physics, PhysicsMeta, GroupPhysics
from .engine import PhysicsEngine
from .static import StaticPhysics
from .kinematic import KinematicPhysics, KinematicPhysicsEngine
from .dynamic import DynamicPhysics, DynamicPhysicsEngine

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
