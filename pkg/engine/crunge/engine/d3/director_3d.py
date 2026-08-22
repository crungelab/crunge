import math

from loguru import logger
import glm

from .scene.scene_3d import Scene3D
from .camera_3d import Camera3D
from .light_3d import Light3D
from ..math import Bounds3


class Director3D:
    """Frames a Scene3D's contents: positions a camera and light so the
    whole scene subtree is visible, and derives parameter ranges (light
    energy/range, position limits) scaled to the scene's extent."""

    def __init__(self, scene: Scene3D) -> None:
        self.scene = scene

    # ------------------------------------------------------------------
    # Scene measurement
    # ------------------------------------------------------------------

    def get_bounds(self) -> Bounds3:
        """Fresh subtree-bounds walk of the whole scene. Not cached - each
        call re-walks the tree, so callers doing multiple things with the
        same bounds (see place_camera_and_light) should compute once and
        pass it down rather than calling this repeatedly."""
        return self.scene.primary_layer.root.get_subtree_bounds()

    def get_max_extent(self, bounds: Bounds3 = None) -> float:
        bounds = bounds if bounds is not None else self.get_bounds()
        size = bounds.size
        return max(size.x, size.y, size.z)

    def get_center(self, bounds: Bounds3 = None) -> glm.vec3:
        bounds = bounds if bounds is not None else self.get_bounds()
        return bounds.center

    def get_target_position(self) -> glm.vec3:
        return self.get_center()

    # ------------------------------------------------------------------
    # Parameter ranges (scaled to scene extent - sliders, gizmo limits, etc.)
    # ------------------------------------------------------------------

    def get_light_position_limits(self):
        bounds = self.get_bounds()
        center = self.get_center(bounds)
        extent = self.get_max_extent(bounds)
        pos_min = [center.x - 2 * extent, center.y - 2 * extent, center.z - 2 * extent]
        pos_max = [center.x + 2 * extent, center.y + 2 * extent, center.z + 2 * extent]
        speed = extent * 0.01
        return (speed, pos_min, pos_max)

    def get_light_energy_limits(self):
        extent = self.get_max_extent()
        energy_min = 0.0
        energy_max = extent ** 2 * 10
        speed = energy_max * 0.01
        return (speed, energy_min, energy_max)

    def get_light_range_limits(self):
        extent = self.get_max_extent()
        range_min = extent * 0.1
        range_max = extent * 5.0
        speed = extent * 0.01
        return (speed, range_min, range_max)

    # ------------------------------------------------------------------
    # Placement
    # ------------------------------------------------------------------

    def place_camera_and_light(self, camera: Camera3D, light: Light3D):
        bounds = self.get_bounds()
        self.place_camera(camera, bounds)
        self.place_light(light, bounds)

    def place_camera(self, camera: Camera3D, bounds: Bounds3 = None):
        bounds = bounds if bounds is not None else self.get_bounds()
        center = self.get_center(bounds)
        max_extent = self.get_max_extent(bounds)

        fov = glm.radians(45.0)
        padding_factor = 1.5
        camera_distance = (max_extent / (2 * math.tan(fov / 2))) * padding_factor

        camera_position = glm.vec3(center.x, center.y, center.z + camera_distance)
        logger.debug(f"Camera position: {camera_position}")

        near_plane = max(max_extent * 0.01, 1e-4)
        far_plane = self._farthest_corner_distance(camera_position, bounds) * 1.5

        camera.position = camera_position
        camera.near = near_plane
        camera.far = far_plane

    def place_light(self, light: Light3D, bounds: Bounds3 = None):
        bounds = bounds if bounds is not None else self.get_bounds()
        center = self.get_center(bounds)
        max_extent = self.get_max_extent(bounds)

        fov = glm.radians(45.0)
        light_distance = (max_extent / (2 * math.tan(fov / 2))) * 0.25

        light.position = glm.vec3(
            center.x + light_distance,
            center.y + light_distance,
            center.z + light_distance,
        )
        light.energy = max_extent ** 2
        light.range = max_extent

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _farthest_corner_distance(point: glm.vec3, bounds: Bounds3) -> float:
        """Distance from `point` to the farthest of the AABB's 8 corners -
        used for a safe far-plane estimate."""
        # ASSUMPTION: Bounds3 exposes `.min`/`.max` as glm.vec3 corners.
        lo, hi = bounds.min, bounds.max
        farthest = 0.0
        for x in (lo.x, hi.x):
            for y in (lo.y, hi.y):
                for z in (lo.z, hi.z):
                    d = glm.length(point - glm.vec3(x, y, z))
                    farthest = max(farthest, d)
        return farthest