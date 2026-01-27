
from dataclasses import dataclass, field

from .stat_channel import StatChannel


@dataclass
class StatGroup:
    """Base for structured stats groups."""
    #name: str
    # Not in __init__; subclasses set a constant default.
    name: str = field(init=False, default="")

    def begin_frame(self) -> None:
        pass

    def end_frame(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def channels(self) -> dict[str, StatChannel]:
        """Return a stable mapping for UI/debug views."""
        return {}
