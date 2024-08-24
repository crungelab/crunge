import glm

class AmbientLight:
    def __init__(self, color=glm.vec3(1.0, 1.0, 1.0), energy=1.0):
        self.color = color
        self.energy = energy
