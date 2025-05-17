from typing import List

from loguru import logger

from crunge import wgpu

from ..base import Base
from ..light import AmbientLight

from .light_3d import Light3D
from .program_3d import Program3D

class Lighting3DProgram(Program3D):
    pass

class Lighting3D(Base):
    def __init__(self):
        self.ambient_light = AmbientLight()
        self.lights: List[Light3D] = []
        self.bind_group: wgpu.BindGroup = None

    def add_light(self, light: Light3D):
        self.lights.append(light)
        self.build_bindgroup()

    def remove_light(self, light: Light3D):
        self.lights.remove(light)

    def build_bindgroup(self):
        logger.debug("Creating bind group for lighting")

        # Light
        light_bg_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.ambient_light.uniform_buffer,
                size=self.ambient_light.uniform_buffer_size,
            )
        ]

        for i, light in enumerate(self.lights):
            light_bg_entries.append(
                wgpu.BindGroupEntry(
                    binding=i + 1,
                    buffer=light.uniform_buffer,
                    size=light.uniform_buffer_size,
                )
            )

        light_bg_desc = wgpu.BindGroupDescriptor(
            label="Light Bind Group",
            layout = Lighting3DProgram().light_bind_group_layout,
            entries=light_bg_entries,
        )

        self.bind_group = self.device.create_bind_group(light_bg_desc)


    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(1, self.bind_group)
