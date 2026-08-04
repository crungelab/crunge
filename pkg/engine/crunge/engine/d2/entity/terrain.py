from loguru import logger

import glm

from crunge.engine.d2.physics.geom import ChainGeom
from crunge.engine.d2.entity import StaticEntity2D


class TerrainChunkModel:
    def __init__(self, points: list[tuple[float, float]]) -> None:
        self.points = points

    @property
    def size(self) -> glm.vec2:
        if not self.points:
            return glm.vec2(0.0, 0.0)
        xs, ys = zip(*self.points)
        return glm.vec2(max(xs) - min(xs), max(ys) - min(ys))


class TerrainChunk(StaticEntity2D):
    def __init__(self, points: list[tuple[float, float]]) -> None:
        model = TerrainChunkModel(points)
        super().__init__(model=model, geom=ChainGeom())
