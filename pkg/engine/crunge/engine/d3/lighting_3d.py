from typing import List

from loguru import logger

from crunge import wgpu

from ..chip import Chip
from ..light import AmbientLight

from .light_3d import Light3D
from .program_3d import Program3D


class Lighting3DProgram(Program3D):
    pass


class Lighting3D(Chip):
    """Owns the light bind group. Seated on the scene, so the ambient
    light's buffer is created by the chip walk rather than by whoever
    remembers to call create().

    The bind group is built lazily. A light registers from `on_added`,
    which runs before the node is created, so its uniform buffer does not
    exist yet — building then produced a bind group over a null buffer.
    """

    def __init__(self):
        super().__init__()
        self.ambient_light = AmbientLight()
        self.lights: List[Light3D] = []
        self.bind_group: wgpu.BindGroup = None
        self._program: Lighting3DProgram = None

    def _create(self):
        super()._create()
        self.ambient_light.create()
        self.mark_binding()

    def _destroy(self):
        self.ambient_light.destroy()
        super()._destroy()

    @property
    def program(self) -> Lighting3DProgram:
        # Was constructed inside build_bindgroup on every rebuild.
        if self._program is None:
            self._program = Lighting3DProgram()
        return self._program

    # -- membership --------------------------------------------------------

    def add_light(self, light: Light3D):
        self.lights.append(light)
        self.mark_binding()

    def remove_light(self, light: Light3D):
        self.lights.remove(light)
        # Was missing: the bind group kept referencing the removed light's
        # buffer, which its chip destroys on teardown.
        self.mark_binding()

    # -- bind group --------------------------------------------------------

    def update(self, delta_time: float) -> None:
        self.flush()

    def _flush_binding(self) -> bool:
        if self.ambient_light.uniform_buffer is None:
            return False
        if any(light.uniform_buffer is None for light in self.lights):
            return False  # a light has not been created yet; retry

        logger.debug("Creating bind group for lighting")

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
            layout=self.program.light_bind_group_layout,
            entries=light_bg_entries,
        )

        self.bind_group = self.device.create_bind_group(light_bg_desc)
        return True

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        # Flush here as well as from update: the renderer binds at
        # begin_pass, and a light added this frame has to be picked up
        # before anything draws through the group.
        self.flush()
        if self.bind_group is None:
            raise RuntimeError(
                f"lighting not ready: ambient="
                f"{self.ambient_light.uniform_buffer is not None} "
                f"lights={[l.uniform_buffer is not None for l in self.lights]}"
            )
        pass_enc.set_bind_group(1, self.bind_group)