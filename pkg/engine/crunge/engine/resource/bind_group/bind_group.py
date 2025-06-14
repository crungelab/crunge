from loguru import logger

from crunge import wgpu

from ..resource import Resource


class BindGroup(Resource):
    def __init__(self, bind_group: wgpu.BindGroup) -> None:
        super().__init__()
        self.bind_group = bind_group

    def get(self) -> wgpu.BindGroup:
        return self.bind_group
