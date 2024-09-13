import glm

from crunge.engine import Vu

class Vu2D(Vu):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)

    @property
    def transform(self):
        return self._transform
    
    @transform.setter
    def transform(self, value):
        self._transform = value
        self.on_transform()

    def on_transform(self):
        pass

    @property
    def size(self):
        raise NotImplementedError
