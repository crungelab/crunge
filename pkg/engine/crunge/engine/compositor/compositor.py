from typing import List

from .passes.base_pass import BasePass

class Compositor:
    def __init__(self):
        self.passes: List[BasePass] = []