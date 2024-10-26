import math
from loguru import logger
import glm
import numpy as np
from crunge import sdl
from ...camera_3d import Camera3D
from .controller import CameraController

class ArcballCameraController(CameraController):
    def __init__(self, window, camera: Camera3D, target=glm.vec3(0.0, 0.0, 0.0), max_extent=1.0):
        super().__init__(window, camera)
        self.target = target
        self.max_extent = max_extent
        self.zoom_speed = max_extent * 0.1
        self.pan_speed = max_extent * 0.05
        self.orbit_radius = max_extent * 1.5

        self.movement_speed = 10.0
        self.mouse_sensitivity = 0.1
        self.first_mouse = True

        # Calculate initial direction and orientation
        dir = target - self.position
        z_axis = glm.normalize(dir)
        x_axis = glm.normalize(glm.cross(z_axis, glm.normalize(self.camera.up)))
        y_axis = glm.normalize(glm.cross(x_axis, z_axis))
        x_axis = glm.normalize(glm.cross(z_axis, y_axis))

        self.camera_target_position = target
        self.camera_position = target - z_axis * self.orbit_radius
        self.orientation = glm.normalize(glm.quat_cast(glm.transpose(glm.mat3(x_axis, y_axis, -z_axis))))

        # Initialize target states for smooth transitions
        self.target_orientation = self.orientation
        self.target_position = self.camera_position

        self.update_camera()

    def activate(self):
        super().activate()
        self.update_camera()

    def rotate(self, prev_mouse: glm.vec2, cur_mouse: glm.vec2):
        cur_mouse = glm.clamp(cur_mouse, glm.vec2(-1, -1), glm.vec2(1, 1))
        prev_mouse = glm.clamp(prev_mouse, glm.vec2(-1, -1), glm.vec2(1, 1))
        mouse_cur_ball = self.screen_to_arcball(cur_mouse)
        mouse_prev_ball = self.screen_to_arcball(prev_mouse)
        self.target_orientation = mouse_cur_ball * mouse_prev_ball * self.orientation        

    def screen_to_arcball(self, p: glm.vec2) -> glm.quat:
        dist = glm.dot(p, p)
        if dist <= 1.0:
            z = np.sqrt(1.0 - dist)
            v = glm.vec3(p.x, p.y, z)
        else:
            v = glm.normalize(glm.vec3(p.x, p.y, 0.0))
        return glm.quat(0.0, v.x, v.y, v.z)

    def pan(self, mouse_delta):
        zoom_amount = abs(glm.length(self.camera_position - self.camera_target_position))
        motion = glm.vec3(mouse_delta.x * zoom_amount, mouse_delta.y * zoom_amount, 0.0)
        self.target_position += motion

    def zoom(self, zoom_amount):
        direction = glm.normalize(self.camera_target_position - self.camera_position)
        self.target_position += direction * self.zoom_speed * zoom_amount

    def update(self, delta_time):
        # Interpolate orientation and position smoothly
        self.orientation = glm.slerp(self.orientation, self.target_orientation, delta_time * 5.0)
        self.camera_position = glm.mix(self.camera_position, self.target_position, delta_time * 5.0)
        self.update_camera()

    def update_camera(self):
        # Update the camera view matrix based on the position and orientation
        view_matrix = glm.translate(glm.mat4(1.0), -self.camera_position) * glm.mat4_cast(self.orientation)
        self.camera.view_matrix = view_matrix
        inverse_view_matrix = glm.inverse(view_matrix)
        self.camera.position = glm.vec3(inverse_view_matrix[3])

    def process_mouse_movement(self, xpos, ypos):
        if self.first_mouse:
            self.prev_mouse = self.transform_mouse(glm.vec2(xpos, ypos), self.width, self.height)
            self.first_mouse = False
        self.rotate(self.prev_mouse, self.transform_mouse(glm.vec2(xpos, ypos), self.width, self.height))

    def transform_mouse(self, pos: glm.vec2, width: int, height: int) -> glm.vec2:
        return glm.vec2(pos.x * 2.0 / width - 1.0, 1.0 - 2.0 * pos.y / height)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        self.zoom(event.y)

    def process_keyboard(self, direction, delta_time):
        velocity = self.movement_speed * delta_time
        if direction == "FORWARD":
            self.zoom(velocity)
        if direction == "BACKWARD":
            self.zoom(-velocity)
        if direction == "LEFT":
            self.pan(glm.vec2(-velocity, 0))
        if direction == "RIGHT":
            self.pan(glm.vec2(velocity, 0))
        self.update_camera()
