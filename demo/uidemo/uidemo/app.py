from pathlib import Path

from crunge import demo
from crunge.demo.menubar import MenubarLocation


resource_root = Path(__file__).parent.parent / 'resources'

class UiDemo(demo.Demo):
    def __init__(self):
        super().__init__("Layout Demo", __package__, resource_root)
        self.menubar_location = MenubarLocation.NAVBAR

