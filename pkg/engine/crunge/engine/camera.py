from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from crunge import wgpu
from crunge.engine import Base

T_Camera = TypeVar("T_Camera")

class CameraAdapter(Base, Generic[T_Camera]):
    def __init__(self, camera: T_Camera) -> None:
        super().__init__()
        self.camera = camera

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass