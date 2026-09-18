from typing import List, Optional

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ...binding import BindGroupLayout, BindGroup

from . import BindGroupIndex


class ModelBindIndex:
    MODEL_UNIFORM = 0


# -- layouts ---------------------------------------------------------------


class ModelBindGroupLayoutBase(BindGroupLayout):
    """Supplies the model entry at binding 0; subclasses add their own.

    `model_buffer_type` is the one thing that varies between model layouts,
    and it is the one thing that made them confusable. A uniform buffer
    holds a single model; a read-only storage buffer holds a group of them
    indexed per instance. Same group index, same binding number,
    incompatible buffer types.

    It is a parameter rather than something a subclass overrides by
    bypassing this class, because bypassing is what hid the divergence: the
    dynamic layout built its entries from scratch and nothing but the label
    said it differed. As an argument, a subclass that diverges has to say
    so on one line, in the open.
    """

    def __init__(
        self,
        entries: Optional[List[wgpu.BindGroupLayoutEntry]] = None,
        model_buffer_type: wgpu.BufferBindingType = wgpu.BufferBindingType.UNIFORM,
        label: str = "Model Bind Group Layout",
    ) -> None:
        entries = list(entries or [])
        entries.append(
            wgpu.BindGroupLayoutEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=model_buffer_type),
            )
        )
        super().__init__(entries=entries, label=label)


@klass.singleton
class ModelBindGroupLayout(ModelBindGroupLayoutBase):
    """One model, in a uniform buffer. For a model that draws itself."""


@klass.singleton
class DynamicModelBindGroupLayout(ModelBindGroupLayoutBase):
    """A group of models, in a read-only storage buffer, indexed per
    instance. For a model whose group draws it."""

    def __init__(self) -> None:
        super().__init__(
            model_buffer_type=wgpu.BufferBindingType.READ_ONLY_STORAGE,
            label="Dynamic Model Bind Group Layout",
        )


# -- bind groups -----------------------------------------------------------


class ModelBindGroupBase(BindGroup):
    """Shared plumbing for every model bind group.

    `layout` is required here, not defaulted. A default made the layout an
    argument a caller could override, and overriding it was the only thing
    separating a per-model bind group from a group-wide one — same class,
    same index, incompatible layouts, and nothing noticed until a pipeline
    rejected one at draw time. Each subclass fixes its own, so the pairing
    cannot come apart.
    """

    def __init__(
        self,
        buffer: wgpu.Buffer,
        buffer_size: int,
        layout: BindGroupLayout,
        entries: Optional[List[wgpu.BindGroupEntry]] = None,
        index: int = BindGroupIndex.MODEL,
        label: str = None,
    ) -> None:
        entries = list(entries or [])
        entries.append(
            wgpu.BindGroupEntry(
                binding=ModelBindIndex.MODEL_UNIFORM,
                buffer=buffer,
                size=buffer_size,
            )
        )
        super().__init__(entries=entries, layout=layout, label=label, index=index)


class ModelBindGroup(ModelBindGroupBase):
    """One model's uniform buffer."""

    def __init__(
        self,
        uniform_buffer: wgpu.Buffer,
        uniform_buffer_size: int,
        entries: Optional[List[wgpu.BindGroupEntry]] = None,
        index: int = BindGroupIndex.MODEL,
        label: str = "Model Bind Group",
    ) -> None:
        super().__init__(
            uniform_buffer,
            uniform_buffer_size,
            layout=ModelBindGroupLayout(),
            entries=entries,
            index=index,
            label=label,
        )


class DynamicModelBindGroup(ModelBindGroupBase):
    """A group's whole model storage buffer."""

    def __init__(
        self,
        storage_buffer: wgpu.Buffer,
        storage_buffer_size: int,
        entries: Optional[List[wgpu.BindGroupEntry]] = None,
        index: int = BindGroupIndex.MODEL,
        label: str = "Dynamic Model Bind Group",
    ) -> None:
        super().__init__(
            storage_buffer,
            storage_buffer_size,
            layout=DynamicModelBindGroupLayout(),
            entries=entries,
            index=index,
            label=label,
        )