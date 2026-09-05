from crunge.engine.chip import Chip

#from .agents.behavioral import BehavioralWyggleAgent as MyAgent
#from .agents.default import DefaultWyggleAgent as MyAgent
#from .agents.neural import NeuralWyggleAgent as MyAgent
from .agents.reactive import ReactiveWyggleAgent as MyAgent

class WyggleMind(Chip):
    def __init__(self):
        super().__init__()
        self.agent: MyAgent = None

    def _enable(self):
        super()._enable()
        self.agent = MyAgent(self.node)
        self.agent.schedule()

    def update(self, delta_time: float):
        self.agent.update(delta_time)
        super().update(delta_time)