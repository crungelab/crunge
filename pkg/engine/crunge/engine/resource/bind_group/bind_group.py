from typing import List

from loguru import logger

from crunge import wgpu

from ..resource import Resource

from .bind_group_layout import BindGroupLayout


class BindGroup(Resource):
    def __init__(
        self,
        layout: BindGroupLayout,
        entries: List[wgpu.BindGroupEntry],
        label: str = None,
        index: int = None,
    ) -> None:
        super().__init__()
        self.layout = layout
        self.entries = entries
        self.label = label
        self.index = index

        bind_group_desc = wgpu.BindGroupDescriptor(
            label=label,
            layout=layout.get(),
            entries=entries,
        )

        self.bind_group: wgpu.BindGroup = self.device.create_bind_group(bind_group_desc)

    def get(self) -> wgpu.BindGroup:
        return self.bind_group
    
    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        """Bind the bind group to the pipeline."""
        pass_enc.set_bind_group(self.index, self.bind_group)


"""
class BindGroup(Resource):
    def __init__(self, bind_group: wgpu.BindGroup) -> None:
        super().__init__()
        self.bind_group = bind_group

    def get(self) -> wgpu.BindGroup:
        return self.bind_group
"""
