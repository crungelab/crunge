from typing import Any

from crunge import wgpu


class RenderState:
    """Redundant-state filter for one render pass.

    Groups issue whatever binds they need through this; it drops the ones
    that would re-set what is already live.

    The dedupe has to live down here rather than in the RenderGroup. Once a
    run is opaque to the RenderGroup — which is what lets a mesh group and a
    sprite group emit different shapes of run — the RenderGroup can no
    longer see what a group is about to bind, and so can no longer filter
    it.
    """

    def __init__(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        self.pass_enc = pass_enc
        self._pipeline = None
        self._bindings: dict[int, Any] = {}

    def set_pipeline(self, program) -> None:
        if program is self._pipeline:
            return
        self._pipeline = program

        # A pipeline change can invalidate every bound group: WebGPU only
        # carries them across a switch when the new layout is compatible
        # with the old one. A cache that survived the switch would skip a
        # set_bind_group the encoder now requires, and that surfaces as a
        # validation error at draw time with nothing pointing back here.
        #
        # Clearing unconditionally is the safe default. If pipelines later
        # turn out to share a layout prefix, groups below the first
        # divergent slot could be kept — but only once the redundant binds
        # are measurable.
        self._bindings.clear()

        self.pass_enc.set_pipeline(program.render_pipeline.get())

    def set_bind_group(self, bind_group) -> None:
        """Bind, unless this exact bind group is already live at its index.

        Keyed on the bind group's OWN index, never one passed in by the
        caller. A slot number at the call site is a second source of truth
        for something BindGroup already knows, and when the two disagree
        the cache treats two writers of one index as independent: it skips
        a bind the pipeline requires, or lets one silently overwrite the
        other and reports it as a layout mismatch three frames away. That
        is how a sprite's ModelBindGroup came to land on top of the dynamic
        sprite group's.

        Identity, not equality. Two bind groups built over the same buffer
        are still two objects and both get bound — correct, if mildly
        wasteful, and the alternative would need an equality that knows
        about layouts, buffers and offsets.
        """
        slot = bind_group.index
        if slot is None:
            raise ValueError(
                f"{bind_group.label or type(bind_group).__name__} has no index; "
                f"a bind group must know which group index it binds to"
            )
        if self._bindings.get(slot) is bind_group:
            return
        self._bindings[slot] = bind_group
        bind_group.bind(self.pass_enc)

    def reset(self) -> None:
        """Forget everything. For a caller that has set pipeline or bind
        group state on the encoder directly, behind this object's back."""
        self._pipeline = None
        self._bindings.clear()