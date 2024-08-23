from crunge import engine

class Controller(engine.Controller):
    def __init__(self, window):
        super().__init__()
        self.window = window
