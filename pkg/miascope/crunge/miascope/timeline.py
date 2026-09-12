"""Stepping and playback over a trace's events, and one-line event descriptions."""

from __future__ import annotations


class Timeline:
    def __init__(self, count: int, rate: float = 10.0):
        self.count = count
        self.t = self.last       # start at the end, showing the whole search
        self.rate = rate         # events per second while playing
        self.playing = False
        self._carry = 0.0

    @property
    def last(self) -> int:
        return max(self.count - 1, 0)

    def seek(self, t: int) -> None:
        self.t = min(max(int(t), 0), self.last)

    def step(self, n: int = 1) -> None:
        self.seek(self.t + n)

    def toggle(self) -> None:
        if self.playing:
            self.playing = False
        else:
            if self.t >= self.last:
                self.t = 0
            self._carry = 0.0
            self.playing = True

    def update(self, dt: float) -> None:
        if not self.playing:
            return
        self._carry += dt * self.rate
        steps = int(self._carry)
        self._carry -= steps
        self.step(steps)
        if self.t >= self.last:
            self.playing = False


def describe(event: dict) -> str:
    kind = event.get("event", "?")
    g = event.get
    match kind:
        case "trace":
            return f"trace of {g('expert')}, started {g('started')}"
        case "space":
            return f"space {g('space')}: {g('expert')} from state {g('root')} ({g('priority')})"
        case "fork":
            plan = f" [{g('plan')}]" if g("plan") else ""
            return f"fork state {g('state')} from {g('parent')}: {g('proposal')}{plan}"
        case "spawn":
            return f"spawn {g('expert')} as state {g('state')}: {g('message')}"
        case "status":
            status = f" {g('status').lower()}" if g("status") else ""
            return f"state {g('state')} {g('step', '').lower()}{status}, cost {g('cost'):g}, priority {g('priority'):g}"
        case "action":
            return f"state {g('state')} records: {g('text')}"
        case "prune":
            return f"prune state {g('state')}: already reached at cost {g('best'):g}"
        case "expand":
            return f"expand state {g('state')} (expansion {g('expansion')})"
        case "skip" | "dead" | "solution":
            return f"{kind} state {g('state')}"
        case "exhausted":
            return f"space {g('space')} hit its expansion limit"
        case "result":
            found = f"solution state {g('solution')}" if g("solution") is not None else "no solution"
            return f"space {g('space')} finished: {found} after {g('expansions')} expansions"
        case _:
            return kind
