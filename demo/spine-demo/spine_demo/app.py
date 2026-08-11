from pathlib import Path

from crunge import demo

resource_root = Path(__file__).parent.parent / "resources"


class SpineDemo(demo.Demo):
    def __init__(self):
        super().__init__("Spine Demo", __package__, resource_root)
