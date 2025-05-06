import time
import math

import glm

from .constants import *


class Camera:
    def __init__(
        self,
        size: glm.ivec2,
        position=glm.vec3(0.0, 0.0, 4.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        yaw=-90.0,
        pitch=0.0,
    ):
        self.size = size
        self.position = position
        self.up = up
        self.yaw = yaw
        self.pitch = pitch
        self.zoom = 45.0

        self.orientation = glm.quat(glm.vec3(0, 0, 0))

        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.update_camera_vectors()

        aspect = float(size.x) / float(size.y)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projection_matrix = glm.perspective(fov_y_radians, aspect, .5, 100.0)
        self.view_matrix = glm.mat4(1.0)

    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix

    def look_at(self, target):
        self.view_matrix = glm.lookAt(self.position, target, self.up)

    def update_camera_vectors(self):
        # Update front, right, and up vectors using the orientation quaternion
        self.front = self.orientation * glm.vec3(0.0, 0.0, -1.0)
        self.right = self.orientation * glm.vec3(1.0, 0.0, 0.0)
        self.up = self.orientation * glm.vec3(0.0, 1.0, 0.0)
