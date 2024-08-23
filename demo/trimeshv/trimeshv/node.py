from .base import Base

from crunge import wgpu

from .camera import Camera


class Node(Base):
    def __init__(self) -> None:
        super().__init__()
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        for child in self.children:
            child.draw(camera, pass_enc)