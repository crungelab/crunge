from ..math.bounds3 import Bounds3
from ..resource.mesh import Mesh

class Mesh3D(Mesh):
    def __init__(self) -> None:
        super().__init__()
        self.bbox = Bounds3()
