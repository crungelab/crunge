from crunge import shell

class Controller(shell.Controller):
    def __init__(self, window):
        super().__init__()
        self.window = window
