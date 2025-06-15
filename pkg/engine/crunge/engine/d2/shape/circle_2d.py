from loguru import logger
import numpy as np
import glm

from ... import colors
from ...color import Color

from .polygon_2d import Polygon2D

class Circle2D(Polygon2D):
    def __init__(
        self,
        center: glm.vec2,
        radius: float,
        segments: int = 32,
        color: Color = colors.WHITE,
    ) -> None:
        """
        Create a Circle2D instance.
        :param center: Center of the circle as glm.vec2.
        :param radius: Radius of the circle.
        :param segments: Number of line segments used to approximate the circle.
        :param color: Color of the circle as glm.vec4.
        """
        self.center = center
        self.radius = radius
        self.segments = segments

        theta = np.linspace(0, 2 * np.pi, self.segments, endpoint=False)
        x = self.center.x + self.radius * np.cos(theta)
        y = self.center.y + self.radius * np.sin(theta)
        points = np.column_stack((x, y))
        super().__init__(points, color)

