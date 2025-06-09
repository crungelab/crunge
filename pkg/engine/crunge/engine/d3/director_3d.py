import math

from loguru import logger
import glm

from .scene_3d import Scene3D
from .camera_3d import Camera3D
from .light_3d import Light3D

class Director3D:
    def __init__(self, scene: Scene3D) -> None:
        self.scene = scene

    def get_max_extent(self) -> float:
        bounds = self.scene.bounds
        size = bounds.size
        max_extent = max(size.x, size.y, size.z)
        logger.debug(f"Model size: {size}, max extent: {max_extent}")
        return max_extent

    def get_center(self) -> glm.vec3:
        bounds = self.scene.bounds
        center = bounds.center
        logger.debug(f"Model center: {center}")
        return center

    def get_target_position(self) -> glm.vec3:
        center = self.get_center()
        logger.debug(f"Model center: {center}")
        return center

    def place_camera_and_light(self, camera: Camera3D, light: Light3D):
        self.place_camera(camera)
        self.place_light(light)

    def place_camera(self, camera: Camera3D):
        max_extent = self.get_max_extent()
        center = self.get_center()
        # Step 3: Set up the camera's field of view (FOV) in radians
        fov = glm.radians(45.0)  # 45 degrees

        # Step 4: Calculate the camera distance
        camera_distance = max_extent / (2 * math.tan(fov / 2))

        # Optional: Add some padding factor to move the camera further back
        padding_factor = 1.5
        camera_distance *= padding_factor

        # Step 5: Position the camera along the z-axis, looking at the model
        camera_position = glm.vec3(center.x, center.y, center.z + camera_distance)
        logger.debug(f"Camera position: {camera_position}")

        # Step 6: Define the near and far planes
        # Set near plane based on a fraction of camera distance or a minimum value
        #near_plane = max(0.1, camera_distance * 0.01)
        near_plane = max_extent * 0.01

        # Calculate distance to farthest point from the camera to determine the far plane
        farthest_point = max_extent - center
        far_plane = glm.length(camera_position - (center + farthest_point)) + max_extent
        far_plane = far_plane * 10

        camera.position = camera_position
        camera.near = near_plane
        camera.far = far_plane

    def place_light(self, light: Light3D):
        max_extent = self.get_max_extent()
        center = self.get_center()
        # Step 3: Set up the camera's field of view (FOV) in radians
        fov = glm.radians(45.0)  # 45 degrees

        # Step 4: Calculate the camera distance
        light_distance = max_extent / (2 * math.tan(fov / 2)) * .25

        light.position = glm.vec3(center.x + light_distance, center.y + light_distance, center.z + light_distance)

        light.range = max_extent  # Adjust the light range as needed
