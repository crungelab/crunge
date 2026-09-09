from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..task import Task
    from ..neuron import Neuron
    from ..agent import Agent

from .scope import Scope


class TaskScope(Scope["Task"]): pass
class NeuronScope(Scope["Neuron"]): pass
class AgentScope(Scope["Agent"]): pass