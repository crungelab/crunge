import time
import math

import glm

from .constants import *

class Camera:
    def __init__(self, size: glm.ivec2) -> None:
        self.size = size
        self.resize(size)

    def resize(self, size: glm.ivec2):
        self.size = size
        aspect = float(size.x) / float(size.y)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

    @property
    def transform_matrix(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        # print(ms)
        viewMatrix = glm.mat4(1.0)
        viewMatrix = glm.translate(viewMatrix, glm.vec3(0, 0, -4))
        viewMatrix = glm.scale(viewMatrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        
        rotMatrix = glm.mat4(1.0)
        rotMatrix = glm.rotate(rotMatrix, math.sin(ms), WORLD_AXIS_X)
        rotMatrix = glm.rotate(rotMatrix, math.cos(ms), WORLD_AXIS_Y)
        return self.projectionMatrix * viewMatrix * rotMatrix
