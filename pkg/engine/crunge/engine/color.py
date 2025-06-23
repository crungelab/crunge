import glm

from .types import Tuple4f

class Color(Tuple4f):
    def __new__(cls, r: float, g: float, b: float, a: float = 1.0):
        return super().__new__(cls, (r, g, b, a))  # type: ignore

    @property
    def r(self) -> float:
        return self[0]

    @property
    def g(self) -> float:
        return self[1]

    @property
    def b(self) -> float:
        return self[2]

    @property
    def a(self) -> float:
        return self[3]

    def to_rgba(self):
        return (self.r, self.g, self.b, self.a)

    def to_argb_int(self):
        #return rgba_tuple_to_argb_int(self.to_rgba())
        return rgba_tuple_to_argb_int(self)

    def to_vec4(self):
        return glm.vec4(self.r, self.g, self.b, self.a)

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


def rgba_tuple_to_argb_int(rgba):
    r, g, b, a = [int(round(x * 255.0)) for x in rgba]
    #r, g, b, a = [int(x * 255.0) for x in rgba]
    return (a << 24) | (r << 16) | (g << 8) | b

def rgba_int_tuple_to_argb_int(rgba):
    r, g, b, a = [int(round(x)) for x in rgba]
    return (a << 24) | (r << 16) | (g << 8) | b
