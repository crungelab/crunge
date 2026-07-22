from .geom import Geom, BoxGeom, BallGeom, HullGeom
#from .physics import Physics, PhysicsMeta, GroupPhysics
from .physics import Physics, GroupPhysics
from .world import PhysicsWorld2D
from .static_physics import StaticPhysics
from .kinematic_physics import KinematicPhysics, KinematicPhysicsEngine
from .dynamic_physics import DynamicPhysics, DynamicPhysicsEngine

# Debug
DEBUG_COLLISION = False

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

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
