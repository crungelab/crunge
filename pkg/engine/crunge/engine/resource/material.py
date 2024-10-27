from crunge import wgpu

from .resource import Resource
from .texture import Texture


class Material(Resource):
    def __init__(self) -> None:
        super().__init__()
