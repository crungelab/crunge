from dataclasses import dataclass, field

from .stat_group import StatGroup
from .timing_stats import TimingStats


@dataclass
class Statistics:
    timing: TimingStats = field(default_factory=TimingStats)
    # counters: CounterStats = field(default_factory=CounterStats)
    # gpu: GpuStats = field(default_factory=GpuStats)  # later

    groups: list[StatGroup] = field(init=False)

    def __post_init__(self) -> None:
        self.groups = [
            self.timing,
            #self.counters,
            # self.gpu,   # later
        ]

    def begin_frame(self) -> None:
        for g in self.groups:
            g.begin_frame()

    def end_frame(self) -> None:
        for g in self.groups:
            g.end_frame()

    def reset(self) -> None:
        for g in self.groups:
            g.reset()
