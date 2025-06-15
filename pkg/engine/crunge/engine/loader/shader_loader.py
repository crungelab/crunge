from typing import Dict

from loguru import logger
from jinja2 import Environment

from crunge import wgpu

from .loader import Loader

class ShaderLoader(Loader):
    def __init__(self, template_env: Environment, template_dict: Dict) -> None:
        super().__init__()
        self.template_env = template_env
        self.template_dict = template_dict


    def load(self, file_name: str) -> wgpu.ShaderModule:
        template = self.template_env.get_template(file_name)
        shader_code = template.render(self.template_dict)
        shader_module = self.gfx.create_shader_module(shader_code)
        return shader_module