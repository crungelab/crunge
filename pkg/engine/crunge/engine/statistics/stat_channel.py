#from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class StatChannel:
    """Tracks one metric with EMA + last + min/max."""

    alpha: float = 0.10
    last: float = 0.0
    ema: float = 0.0
    min: float = math.inf
    max: float = -math.inf
    count: int = 0

    def push(self, x: float) -> None:
        self.last = x
        if self.count == 0:
            self.ema = x
            self.min = x
            self.max = x
        else:
            self.ema = self.alpha * x + (1.0 - self.alpha) * self.ema
            if x < self.min:
                self.min = x
            if x > self.max:
                self.max = x
        self.count += 1

    def reset(self) -> None:
        self.last = 0.0
        self.ema = 0.0
        self.min = math.inf
        self.max = -math.inf
        self.count = 0
