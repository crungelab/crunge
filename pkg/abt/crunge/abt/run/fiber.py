from .task import Task

class Fiber:
    def __init__(self, task: Task | None = None, parent: "Fiber" | None = None):
        self.parent = parent
        self.children: list["Fiber"] = []
        self.task: Task | None = task
        if parent:
            parent.add(self)

    def cancel(self):
        for child in tuple(self.children):
            child.cancel()
        if self.task is not None and not self.task.status.done:
            self.task.cancel()