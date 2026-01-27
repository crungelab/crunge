from dataclasses import dataclass, field

from .stat_channel import StatChannel
from .stat_group import StatGroup

_EPS = 1e-12


@dataclass
class TimingStats(StatGroup):
    name: str = field(init=False, default="Timing")

    update_s: StatChannel = field(default_factory=lambda: StatChannel(alpha=0.10))
    render_s: StatChannel = field(default_factory=lambda: StatChannel(alpha=0.10))
    frame_s: StatChannel = field(default_factory=lambda: StatChannel(alpha=0.10))

    fps: StatChannel = field(default_factory=lambda: StatChannel(alpha=0.20))
    fps_instant: float = 0.0

    def push_frame(self, update_s: float, render_s: float, frame_s: float) -> None:
        self.update_s.push(max(0.0, update_s))
        self.render_s.push(max(0.0, render_s))
        self.frame_s.push(max(_EPS, frame_s))

        dt = max(_EPS, self.frame_s.last)
        self.fps_instant = 1.0 / dt
        self.fps.push(self.fps_instant)

    @property
    def update_ms(self) -> float:
        return self.update_s.ema * 1000.0

    @property
    def render_ms(self) -> float:
        return self.render_s.ema * 1000.0

    @property
    def frame_ms(self) -> float:
        return self.frame_s.ema * 1000.0

    def reset(self) -> None:
        self.update_s.reset()
        self.render_s.reset()
        self.frame_s.reset()
        self.fps.reset()
        self.fps_instant = 0.0

    def channels(self) -> dict[str, StatChannel]:
        return {
            "update_s": self.update_s,
            "render_s": self.render_s,
            "frame_s": self.frame_s,
            "fps": self.fps,
        }
