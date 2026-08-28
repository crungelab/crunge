class Dirt(IntFlag):
    """What a chip owes the next flush.

    One member per thing that gets rebuilt independently. Transform is not
    a member: the node owns the transform and already tracks its own dirty
    state, so a second flag here would be a duplicate source of truth.
    """

    NONE = 0
    GEOMETRY = auto()  # vertex/index data the chip owns
    BINDING = auto()  # bind groups, which reference the buffers below
    GPU = auto()  # uniform data the chip owns


# --- and inside Chip, replacing the existing mark/flush block: ---

    def mark_geometry(self) -> None:
        self.mark(Dirt.GEOMETRY)

    def mark_binding(self) -> None:
        self.mark(Dirt.BINDING)

    def mark_gpu(self) -> None:
        self.mark(Dirt.GPU)

    def flush(self) -> None:
        """Rebuild whatever is owed. Safe every frame; cheap when clean.

        Explicit per-domain dispatch rather than a table: the order between
        domains is load-bearing, and a rebuild that feeds another has to
        run first. Geometry before binding, since vertex data can change
        what a bind group describes; binding before the uniform write,
        since a bind group has to exist before anything reads through it.
        """
        dirt = self._dirt
        if dirt is Dirt.NONE:
            return

        if dirt & Dirt.GEOMETRY and self._flush_geometry():
            self._dirt &= ~Dirt.GEOMETRY

        if dirt & Dirt.BINDING and self._flush_binding():
            self._dirt &= ~Dirt.BINDING

        if dirt & Dirt.GPU and self._flush_gpu():
            self._dirt &= ~Dirt.GPU

    def _flush_geometry(self) -> bool:
        """Rebuild vertex/index data. Return False if the target is not
        there yet — the flag stays set and retries on the next flush."""
        return True

    def _flush_binding(self) -> bool:
        """Rebuild bind groups. Return False if a resource they reference
        does not exist yet — the flag stays set and retries."""
        return True

    def _flush_gpu(self) -> bool:
        """Write uniform data. Return False if the target is not there yet
        — the flag stays set and retries on the next flush."""
        return True