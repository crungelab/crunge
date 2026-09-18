from loguru import logger

from crunge import wgpu
from crunge.core import klass

from .model import ModelBindGroupLayoutBase, ModelBindGroupBase
from . import BindGroupIndex


class EmitterBindIndex:
    MODEL_UNIFORM = 0
    PARTICLE_STORAGE = 1


# Fragment — the two emitter classes only.

@klass.singleton
class EmitterBindGroupLayout(ModelBindGroupLayoutBase):
    """Model uniform plus the emitter's particle storage buffer.

    Unchanged: the base still appends the model entry at binding 0, so this
    declares only what it adds.
    """

    def __init__(self) -> None:
        entries = [
            wgpu.BindGroupLayoutEntry(
                binding=EmitterBindIndex.PARTICLE_STORAGE,
                visibility=wgpu.ShaderStage.COMPUTE | wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]

        super().__init__(entries=entries, label="Emitter Bind Group Layout")


class EmitterBindGroup(ModelBindGroupBase):
    """Model uniform plus the emitter's particle storage buffer.

    Over the base rather than ModelBindGroup: it is a third model binding at
    the same index with its own layout, not a variant of the single-model
    one. The base supplies the model uniform entry; this adds the particle
    storage entry and fixes the layout that describes both.
    """

    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        storage_buffer: wgpu.Buffer,
        storage_buffer_size: int,
        index: int = BindGroupIndex.MODEL,
        label: str = "Emitter Bind Group",
    ) -> None:
        entries = [
            wgpu.BindGroupEntry(
                binding=EmitterBindIndex.PARTICLE_STORAGE,
                buffer=storage_buffer,
                size=storage_buffer_size,
            ),
        ]
        # layout is no longer a parameter — it was only ever overridable by
        # accident, and overriding it is what let two incompatible layouts
        # share one class.
        super().__init__(
            uniform_buffer,
            uniform_buffer_size,
            layout=EmitterBindGroupLayout(),
            entries=entries,
            index=index,
            label=label,
        )