from typing import Any

from crunge import wgpu


class RenderState:
    """Redundant-state filter for one render pass.

    Groups issue whatever binds they need through this; it drops the ones
    that would re-set what is already live.

    The dedupe has to live down here rather than in the RenderGroup. Once a
    run is opaque to the RenderGroup — which is what lets a mesh group and a
    sprite group emit different shapes of run — the RenderGroup can no longer
    see what a group is about to bind, and so can no longer filter it.
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

    def set_bind_group(self, slot: int, bind_group) -> None:
        """For bind groups that know their own binding index.

        `slot` is bookkeeping for this cache only — the actual index comes
        from the bind group itself, inside its bind().
        """
        if self._bindings.get(slot) is bind_group:
            return
        self._bindings[slot] = bind_group
        bind_group.bind(self.pass_enc)

    def claim(self, slot: int, key: Any) -> bool:
        """For binds that need arguments this cache can't supply.

        Returns True when `key` differs from what is live in `slot`, and
        records it; the caller does the binding itself. Use it when the bind
        call needs more than the bind group — a membership index, a dynamic
        offset — so the caller stays in control of the call while the
        filtering still happens in one place.
        """
        if self._bindings.get(slot) is key:
            return False
        self._bindings[slot] = key
        return True

    def reset(self) -> None:
        self._pipeline = None
        self._bindings.clear()
