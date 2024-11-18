import glm
from numpy import ndarray

from ..resource import Resource

class Image(Resource):
    def __init__(self, data: ndarray):
        super().__init__()
        self.data = data

    @property
    def size(self) -> glm.ivec2:
        #return self.data.shape[:2]
        return glm.ivec2(self.width, self.height)
    
    @property
    def width(self):
        return self.data.shape[1]
    
    @property
    def height(self):
        return self.data.shape[0]