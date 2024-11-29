from loguru import logger

from crunge import wgpu

from ..resource import Resource


class BindGroupLayout(Resource):
    def __init__(self, bind_group_layout: wgpu.BindGroupLayout) -> None:
        super().__init__()
        self.bind_group_layout = bind_group_layout

    def get(self) -> wgpu.BindGroupLayout:
        return self.bind_group_layout
