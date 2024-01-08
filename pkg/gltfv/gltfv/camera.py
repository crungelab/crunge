import time
import math

import glm

from .constants import *

class Camera:
    def __init__(self, width, height) -> None:
        aspect = float(width) / float(height)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)
        self.transform_matrix = glm.mat4(1.0)

    def update(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        # print(ms)
        view_matrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 0, -4))
        view_matrix = glm.scale(view_matrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE))
        
        rot_matrix = glm.rotate(glm.mat4(1.0), math.sin(ms), WORLD_AXIS_X)
        rot_matrix = glm.rotate(rot_matrix, math.cos(ms), WORLD_AXIS_Y)
        self.view_matrix = view_matrix * rot_matrix

        self.transform_matrix = self.projection_matrix * self.view_matrix
