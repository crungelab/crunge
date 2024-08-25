from typing import List
from .light_3d import Light3D


class Lighting3D:
    def __init__(self):
        self.lights: List[Light3D] = []

    def add_light(self, light: Light3D):
        self.lights.append(light)

    def remove_light(self, light: Light3D):
        self.lights.remove(light)

    def apply(self, renderer):
        for light in self.lights:
            light.apply()