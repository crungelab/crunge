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
            return f"trace of {g('agent')}, started {g('started')}"
        case "agency":
            return f"search {g('agency')}: {g('agent')} from agent {g('root')} ({g('priority')})"
        case "fork":
            plan = f" [{g('plan')}]" if g("plan") else ""
            return f"fork agent {g('agent')} from {g('parent')}: {g('proposal')}{plan}"
        case "spawn":
            return f"spawn {g('expert')} as agent {g('agent')}: {g('message')}"
        case "state":
            status = f" {g('status').lower()}" if g("status") else ""
            return f"agent {g('agent')} {g('step', '').lower()}{status}, cost {g('cost'):g}, priority {g('priority'):g}"
        case "prune":
            return f"prune agent {g('agent')}: state already reached at cost {g('best'):g}"
        case "expand":
            return f"expand agent {g('agent')} (expansion {g('expansion')})"
        case "skip" | "dead" | "solution":
            return f"{kind} agent {g('agent')}"
        case "exhausted":
            return f"search {g('agency')} hit its expansion limit"
        case "result":
            found = f"solution agent {g('solution')}" if g("solution") is not None else "no solution"
            return f"search {g('agency')} finished: {found} after {g('expansions')} expansions"
        case _:
            return kind
