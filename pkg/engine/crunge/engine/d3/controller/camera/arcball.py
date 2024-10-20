import math

from loguru import logger
import glm
import numpy as np

from crunge import sdl
from ...camera_3d import Camera3D

from .controller import CameraController

import glm

def screen_to_arcball(p: glm.vec2) -> glm.quat:
    dist = glm.dot(p, p)
    if dist <= 1.0:
        return glm.quat(0.0, p.x, p.y, np.sqrt(1.0 - dist))
    else:
        proj = glm.normalize(p)
        return glm.quat(0.0, proj.x, proj.y, 0.0)
    
def transform_mouse(pos: glm.vec2, width: int, height: int) -> glm.vec2:
    return glm.vec2(pos.x * 2.0 / width - 1.0, 1.0 - 2.0 * pos.y / height)


class ArcballCameraController(CameraController):
    def __init__(self, window, camera: Camera3D, target=glm.vec3(0.0, 0.0, 0.0), radius=1.0):
        super().__init__(window, camera)
        self.target = target
        self.radius = radius
        self.distance = glm.length(camera.position - target)
        self.movement_speed = 10.0
        self.mouse_sensitivity = 20.0
        self.first_mouse = True

    
        dir = target - self.position
        z_axis = glm.normalize(dir)
        x_axis = glm.normalize(glm.cross(z_axis, glm.normalize(self.camera.up)))
        y_axis = glm.normalize(glm.cross(x_axis, z_axis))
        x_axis = glm.normalize(glm.cross(z_axis, y_axis))

        self.target_translation = glm.inverse(glm.translate(glm.mat4(1.0), target))
        self.translation = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -glm.length(dir)))
        self.orientation = glm.normalize(glm.quat_cast(glm.transpose(glm.mat3(x_axis, y_axis, -z_axis))))

        self.update_camera()

    def activate(self):
        super().activate()
        self.update_camera()


    def rotate(self, prev_mouse, cur_mouse):
        cur_mouse = glm.clamp(cur_mouse, glm.vec2(-1, -1), glm.vec2(1, 1))
        prev_mouse = glm.clamp(prev_mouse, glm.vec2(-1, -1), glm.vec2(1, 1))

        mouse_cur_ball = screen_to_arcball(cur_mouse)
        mouse_prev_ball = screen_to_arcball(prev_mouse)

        self.orientation = mouse_cur_ball * mouse_prev_ball * self.orientation
        self.update_camera()

    def pan(self, mouse_delta):
        zoom_amount = abs(self.translation[3][2])
        motion = glm.vec4(mouse_delta.x * zoom_amount, mouse_delta.y * zoom_amount, 0.0, 0.0)

        self.target_translation = glm.translate(glm.mat4(1.0), glm.vec3(motion)) * self.target_translation
        self.update_camera()

    def zoom(self, zoom_amount):
        motion = glm.vec3(0.0, 0.0, zoom_amount)
        self.translation = glm.translate(glm.mat4(1.0), motion) * self.translation
        self.update_camera()
    
    def update_camera(self):
        self.camera.view_matrix = self.translation * glm.mat4_cast(self.orientation) * self.target_translation
        inverse_view_matrix = glm.inverse(self.camera.view_matrix)
        self.camera.position = glm.vec3(inverse_view_matrix[3])

    def process_mouse_movement(self, xpos, ypos):
        #logger.debug(f"Mouse movement: {xpos}, {ypos}")

        if self.first_mouse:
            self.prev_mouse = transform_mouse(glm.vec2(xpos, ypos), self.width, self.height)
            self.first_mouse = False
        # Perform the rotation
        self.rotate(self.prev_mouse, transform_mouse(glm.vec2(xpos, ypos), self.width, self.height))

        #logger.debug(f"Camera position: {self.camera.position}")
        #logger.debug(f"Camera orientation: {self.camera.orientation}")

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        self.zoom(event.y * 0.1)

    def process_keyboard(self, direction, delta_time):
        logger.debug(f"Keyboard: {direction}, {delta_time}")
        velocity = self.movement_speed * delta_time
        logger.debug(f"Velocity: {velocity}")
        self.camera.update_camera_vectors()
        if direction == "FORWARD":
            self.zoom(velocity)
        if direction == "BACKWARD":
            self.zoom(-velocity)
        if direction == "LEFT":
            self.pan(glm.vec2(-velocity, 0))
        if direction == "RIGHT":
            self.pan(glm.vec2(velocity, 0))
        self.update_camera()
