from enum import Enum


class MotionState(Enum):
    GROUNDED = 0
    JUMPING = 1
    CLIMBING = 2
    FALLING = 3
    MOUNTED = 4
