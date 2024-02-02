from loguru import logger

import glm

from ...sprite import Sprite
#from ...node_2d import Node2D
from ...model_2d import DynamicModel2D
from ...texture_atlas_kit import TextureAtlasKit
from ...resource_kit import ResourceKit
from ...geom import BoxGeom

class Ship(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        path = ResourceKit().root / "spaceshooter" / "sheet.xml"
        atlas = TextureAtlasKit().load(path)
        logger.debug(f"atlas: {atlas}")
        
        texture = atlas.get("playerShip1_orange.png")

        self.vu = Sprite(texture)
        self.position = position
        self.size = texture.size

    def update(self, dt):
        super().update(dt)
        self.body.apply_force_at_local_point((0, 100), (0, 0))
