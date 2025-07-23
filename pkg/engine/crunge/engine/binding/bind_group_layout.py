from typing import List

from loguru import logger

from crunge import wgpu

from ..base import Base


class BindGroupLayout(Base):
    def __init__(
        self,
        entries: List[wgpu.BindGroupEntry],
        label: str = None,
    ) -> None:
        super().__init__()
        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=entries, label=label)
        self.bind_group_layout = self.device.create_bind_group_layout(bgl_desc)

    def get(self) -> wgpu.BindGroupLayout:
        return self.bind_group_layout
