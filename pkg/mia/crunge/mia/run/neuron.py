import types
from typing import Optional, Callable

from loguru import logger

from .scope import AgentScope, NeuronScope


class Neuron:
    """Activity source for an Act. Composes into a tree of its own."""

    def __init__(self):
        self.children: list["Neuron"] = []

        self.agent = AgentScope.top()
        self.parent: Optional["Neuron"] = NeuronScope.top()
        if self.parent:
            self.parent.add(self)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __enter__(self) -> "Neuron":
        if self.parent is None:
            parent = NeuronScope.top()
            if parent is not None:
                parent.add(self)
        NeuronScope.push(self)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        NeuronScope.pop(self)
        return False

    #
    # TREE
    #
    def add(self, child: "Neuron") -> "Neuron":
        child.parent = self
        if child.agent is None:
            child.agent = self.agent
        self.children.append(child)
        return self

    def remove(self, child: "Neuron") -> "Neuron":
        try:
            self.children.remove(child)
        except ValueError:
            logger.warning("Not a child of {}: {}", self, child)
        return self

    #
    # ACTIVITY
    #
    @property
    def activity(self) -> float:
        return self.main()

    def enable(self):
        pass

    def disable(self):
        pass

    def main(self) -> float:
        return 1

    def use(self, fn: Callable):
        self.main = types.MethodType(fn, self)


# DSL
def neuron(neuron=None):
    return neuron if neuron is not None else Neuron()
