from loguru import logger

from crunge.engine.d2.particle.system import ParticleSystem2D

from .explosion_program import ExplosionProgram


class ExplosionVu(ParticleSystem2D):
    def __init__(self, color=(0.0, 0.0, 1.0, 1.0)):
        super().__init__(program=ExplosionProgram(), color=color)
