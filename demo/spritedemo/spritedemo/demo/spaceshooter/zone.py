from scipy.stats.qmc import PoissonDisk

from loguru import logger
import glm

from crunge.engine import Base

from .meteor import Meteor, MeteorGreyBig1

class Zone(Base):
    def __init__(self, scene, position: glm.vec2, size: glm.vec2, safe_radius: float = 400.0):
        super().__init__()
        self.scene = scene
        self.position = position
        self.size = size
        self.safe_radius = safe_radius

    @property
    def width(self):
        return self.size.x
    
    @property
    def height(self):
        return self.size.y
    
    def _create(self) -> None:
        super()._create()
        self.create_meteors(100)

    def create_meteor(self, position: glm.vec2):
        meteor = MeteorGreyBig1(position).create()
        self.scene.attach(meteor)

    def create_meteors(self, num_asteroids):
        """
        Generates an asteroid field using Poisson Disk sampling.

        Args:
            num_asteroids (int): Number of asteroids to generate.
            safe_radius (float): Radius of the safe zone around the ship.
            min_radius (float): Minimum radius of the asteroids.
            max_radius (float): Maximum radius of the asteroids.
            bounds (tuple): Boundaries of the generation area ((xmin, ymin), (xmax, ymax)).
        """

        def check_ship_distance(point: glm.vec2, other_point: glm.vec2):
            return glm.distance(point, self.ship.position) > self.safe_radius

        sampler = PoissonDisk(d=2, radius=.1)

        samples = sampler.random(num_asteroids)
        #logger.debug(f"samples: {samples}")

        # 4. Create asteroids within original bounds
        for sample in samples:
            xi, yi = sample
            #logger.debug(f"xi: {xi}, yi: {yi}")
            x = (self.position.x - self.width) + (xi * self.width * 2)
            y = (self.position.y - self.height) + (yi * self.height * 2)
            point = glm.vec2(x, y)
            if glm.distance(point, self.position) > self.safe_radius:
                self.create_meteor(point)
