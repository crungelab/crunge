import os
from pathlib import Path

from loguru import logger
import glm

from crunge import demo


resource_root = Path(__file__).parent.parent / 'resources'

class ImGuiDemo(demo.Demo):
    def __init__(self):
        super().__init__("ImGui Demo", resource_root)
