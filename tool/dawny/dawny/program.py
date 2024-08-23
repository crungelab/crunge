from .frontend import Frontend
from .backend import Backend
from .node import Root

class Program():
    def __init__(self) -> None:
        self.root:Root = None # Set by Frontend
        self.frontend = Frontend(self)
        self.backend = Backend(self)

    def run(self):
        self.frontend.run()
        self.backend.run()