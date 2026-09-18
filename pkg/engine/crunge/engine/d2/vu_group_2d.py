from loguru import logger

from crunge import wgpu

from ..buffer import UniformBuffer
from ..vu_group import VuGroup, Run, ELEMENTS

from .vu_2d import Vu2D
from .uniforms_2d import NodeUniform
from .binding_2d import NodeBindGroup


class VuGroup2D[VuT: Vu2D](VuGroup[VuT]):
    """A VuGroup that owns a node uniform buffer and its bind group.

    Split out of the base so the base can stay free of d2 imports: the
    engine root imports node -> render_group -> vu_group, and d2 imports the
    engine root back. This class sits on the d2 side of that edge, which is
    the only place that can see both a VuGroup and a NodeUniform.

    One program, therefore one bind group layout, therefore one node buffer
    and one bind group. That invariant is what makes a group the unit a run
    cannot span: first_instance indexes whatever buffer is bound at draw
    time.
    """

    def __init__(self, count: int = ELEMENTS, program=None) -> None:
        super().__init__(count, program)
        self.node_bind_group: NodeBindGroup = None
        self.node_buffer = UniformBuffer(
            NodeUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label=f"{self.__class__.__name__} Node Buffer",
        )
        logger.debug(f"Node Uniform Buffer: {self.node_buffer}")

    # -- lifetime ----------------------------------------------------------

    def _create(self) -> None:
        super()._create()
        self.create_bind_groups()

    def create_bind_groups(self) -> None:
        self.node_bind_group = NodeBindGroup(
            self.node_buffer.get(),
            self.node_buffer.size,
            layout=self.program.render_pipeline.node_bind_group_layout,
        )

    def destroy(self) -> None:
        super().destroy()
        self.node_bind_group = None

    # -- membership --------------------------------------------------------

    def append(self, vu: VuT) -> None:
        super().append(vu)
        vu.node_buffer = self.node_buffer
        # Explicit sentinel. Vu2D starts at 0, which is a real slot — without
        # this the vu writes over whoever actually owns slot 0 for the one
        # frame between appending and the next replan. The slot itself is
        # assigned by the RenderGroup, because append order is not draw order.
        vu.node_buffer_index = -1

    def remove(self, vu: VuT) -> None:
        super().remove(vu)
        vu.node_buffer_index = -1
        vu.node_buffer = None

    # -- planning ----------------------------------------------------------

    def place(self, vu: VuT, slot: int) -> None:
        """Guarded, because replan runs over every member and most slots do
        not move. Without the guard, one sprite moving re-uploads the whole
        buffer."""
        if vu.node_buffer_index == slot:
            return
        # Setter marks GPU dirt; the write lands on the next flush.
        vu.node_buffer_index = slot

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        self.node_bind_group.bind(pass_enc)