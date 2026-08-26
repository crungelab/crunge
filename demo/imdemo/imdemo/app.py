from pathlib import Path

from crunge import demo


resource_root = Path(__file__).parent.parent / 'resources'

class ImGuiDemo(demo.Demo):
    def __init__(self):
        super().__init__("ImGui Demo", __package__, resource_root)
