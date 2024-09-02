from numpy import ndarray


class Image:
    def __init__(self, data: ndarray):
        self.data = data

    @property
    def width(self):
        return self.data.shape[1]
    
    @property
    def height(self):
        return self.data.shape[0]