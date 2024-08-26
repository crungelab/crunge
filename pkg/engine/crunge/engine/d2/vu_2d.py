import glm

from crunge.engine import Vu

class Vu2D(Vu):
    def __init__(self) -> None:
        super().__init__()
        self.transform = glm.mat4(1.0)

    @property
    def size(self):
        raise NotImplementedError
