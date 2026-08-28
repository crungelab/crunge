from loguru import logger
from ctypes import sizeof

import glm

from crunge import wgpu

from ..uniforms import cast_vec3
from ..signal import Pulse
from ..chip import Chip
from .node_3d import Node3D

from .uniforms_3d import (
    LightUniform,
)


class LightChip(Chip["Light3D"]):
    """Owns the light's uniform buffer.

    Split out of Light3D because a node holding a GPU buffer is what chips
    are for: the buffer now rides the create/enable/destroy walk instead of
    being allocated in a constructor, and the write is deferred like every
    other GPU write in the engine.
    """

    def __init__(self) -> None:
        super().__init__()
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

    def _create(self) -> None:
        super()._create()
        self.uniform_buffer_size = sizeof(LightUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Light Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
        )

    # -- listening ---------------------------------------------------------

    def listen(self) -> None:
        node = self.node
        node.transform_changed.connect(self.on_transform_changed)
        node.light_changed.connect(self.mark_gpu)

    def deafen(self) -> None:
        node = self._node
        if node is None:
            return
        node.transform_changed.disconnect(self.on_transform_changed)
        node.light_changed.disconnect(self.mark_gpu)

    def sync(self) -> None:
        self.mark_gpu()

    def on_transform_changed(self, node: "Light3D") -> None:
        self.mark_gpu()

    # -- deferred upload ---------------------------------------------------

    def update(self, delta_time: float) -> None:
        self.flush()

    def _flush_gpu(self) -> bool:
        if self.uniform_buffer is None:
            return False

        node = self.node
        light_uniform = LightUniform()
        light_uniform.position = cast_vec3(node.global_position)
        light_uniform.color = cast_vec3(node.color)
        light_uniform.energy = node.energy
        light_uniform.range = node.range

        self.gfx.device.queue.write_buffer(self.uniform_buffer, 0, light_uniform)
        return True


class Light3D(Node3D):
    def __init__(
        self,
        position: glm.vec3 = None,
        color: glm.vec3 = None,
        energy: float = 1.0,
        range: float = 10.0,
    ) -> None:
        super().__init__(position=position)
        # None sentinel: a glm.vec3 default is one shared mutable instance
        # across every light ever constructed.
        self._color = glm.vec3(1.0, 1.0, 1.0) if color is None else glm.vec3(color)
        self._energy = energy
        self._range = range

        # Payload-free: the chip reads the three values off the node when
        # it flushes, and there is exactly one subscriber.
        self.light_changed = Pulse()

    def _seat(self) -> None:
        super()._seat()
        if not self.has(LightChip):
            self.add(LightChip())

    @property
    def uniform_buffer(self) -> wgpu.Buffer:
        """Forwarded so the lighting system keeps reading it off the node."""
        chip = self.get(LightChip)
        return chip.uniform_buffer if chip is not None else None

    @property
    def uniform_buffer_size(self) -> int:
        chip = self.get(LightChip)
        return chip.uniform_buffer_size if chip is not None else 0

    # -- properties --------------------------------------------------------

    @property
    def color(self) -> glm.vec3:
        return self._color

    @color.setter
    def color(self, color: glm.vec3) -> None:
        self._color = color
        self.light_changed.emit()

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, energy: float) -> None:
        self._energy = energy
        self.light_changed.emit()

    @property
    def range(self) -> float:
        return self._range

    @range.setter
    def range(self, range: float) -> None:
        self._range = range
        self.light_changed.emit()

    # -- scene membership --------------------------------------------------

    def on_added(self):
        self.scene.lighting.add_light(self)
        super().on_added()

    def on_removed(self):
        self.scene.lighting.remove_light(self)
        super().on_removed()


class OmniLight3D(Light3D):
    pass