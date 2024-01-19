import math

from loguru import logger
import glm
import numpy as np
import glfw

from ...camera import Camera

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
    def __init__(self, window, camera: Camera, target=glm.vec3(0.0, 0.0, 0.0), radius=1.0):
        super().__init__(window, camera)
        self.target = target
        self.radius = radius
        self.distance = glm.length(camera.position - target)
        self.movement_speed = 2.5
        self.mouse_sensitivity = 20.0
        self.first_mouse = True
        self.width = 0
        self.height = 0

        #dir = center - eye
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
        #self.width, self.height = glfw.get_framebuffer_size(self.window)
        self.width, self.height = glfw.get_window_size(self.window)


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
        motion = glm.inverse(self.camera) * motion

        self.target_translation = glm.translate(glm.mat4(1.0), glm.vec3(motion)) * self.target_translation
        self.update_camera()

    def zoom(self, zoom_amount):
        motion = glm.vec3(0.0, 0.0, zoom_amount)
        self.translation = glm.translate(glm.mat4(1.0), motion) * self.translation
        self.update_camera()

    def transform(self):
        return self.camera

    def inv_transform(self):
        return self.inv_camera

    def eye(self):
        return glm.vec3(self.inv_camera * glm.vec4(0, 0, 0, 1))

    def dir(self):
        return glm.normalize(glm.vec3(self.inv_camera * glm.vec4(0, 0, -1, 0)))

    def up(self):
        return glm.normalize(glm.vec3(self.inv_camera * glm.vec4(0, 1, 0, 0)))

    def update_camera(self):
        #self.camera = self.translation * glm.mat4_cast(self.rotation) * self.target_translation
        self.camera.view_matrix = self.translation * glm.mat4_cast(self.orientation) * self.target_translation
        self.inv_camera = glm.inverse(self.camera.view_matrix)

    def process_mouse_movement(self, xpos, ypos):
        #logger.debug(f"Mouse movement: {xpos}, {ypos}")

        if self.first_mouse:
            self.prev_mouse = transform_mouse(glm.vec2(xpos, ypos), self.width, self.height)
            self.first_mouse = False
        # Perform the rotation
        self.rotate(self.prev_mouse, transform_mouse(glm.vec2(xpos, ypos), self.width, self.height))

        self.position = self.target + self.orientation * glm.vec3(0, 0, -1) * self.distance

        #logger.debug(f"Camera position: {self.camera.position}")
        #logger.debug(f"Camera orientation: {self.camera.orientation}")

        #self.camera.update_camera_vectors()
        #self.camera.look_at(self.target)

    def on_scroll(self, window, xoffset, yoffset):
        self.zoom(yoffset * 0.1)

    def process_keyboard(self, direction, delta_time):
        velocity = self.movement_speed * delta_time
        if direction == "FORWARD":
            self.camera.position += self.camera.front * velocity
        if direction == "BACKWARD":
            self.camera.position -= self.camera.front * velocity
        if direction == "LEFT":
            self.camera.position -= self.camera.right * velocity
        if direction == "RIGHT":
            self.camera.position += self.camera.right * velocity

    '''
    def on_cursor_pos(self, window, xpos, ypos):
        if not self.mouse_captured:
            return
        self.process_mouse_movement(xpos, ypos)

    def on_mouse_button(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                self.mouse_captured = True
                self.first_mouse = True
            elif action == glfw.RELEASE:
                #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                self.mouse_captured = False


    def on_key(self, window, key, scancode, action, mods):
        if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
            self.process_keyboard('FORWARD', self.delta_time)
        if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
            self.process_keyboard('BACKWARD', self.delta_time)
    '''