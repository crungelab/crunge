from typing import TypeAlias

import glm

Vector2: TypeAlias = glm.vec2
Vector2i: TypeAlias = glm.ivec2

Point2: TypeAlias = glm.vec2
Point2i: TypeAlias = glm.ivec2

Size2: TypeAlias = glm.vec2
Size2i: TypeAlias = glm.ivec2

Vector3: TypeAlias = glm.vec3
Vector3i: TypeAlias = glm.ivec3
 
Point3: TypeAlias = glm.vec3
Point3i: TypeAlias = glm.ivec3

Size3: TypeAlias = glm.vec3
Size3i: TypeAlias = glm.ivec3

from .rect import Rect2, Rect2i
from .bounds3 import Bounds3