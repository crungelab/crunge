from crunge.engine.chip import Chip

from .agents.reactive import ReactiveWyggleAgent

class WyggleMind(Chip):
    def __init__(self):
        super().__init__()
        self.agent: ReactiveWyggleAgent = None

    def _enable(self):
        super()._enable()
        self.agent = ReactiveWyggleAgent(self.node)
        self.agent.schedule()

    def update(self, delta_time: float):
        self.agent.update(delta_time)
        super().update(delta_time)