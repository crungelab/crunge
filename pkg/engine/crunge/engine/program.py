from typing import List

from loguru import logger
from jinja2 import Environment, BaseLoader, ChoiceLoader, PackageLoader, select_autoescape

from crunge.engine import Base


class Program(Base):
    def __init__(self, template_loaders: List[BaseLoader] = []):
        self.template_loader_stack: List[BaseLoader] = [PackageLoader("crunge.engine", "templates")]
        self.template_loader_stack.extend(template_loaders)

        self.update_template_env()

    def push_template_loader(self, loader: BaseLoader):
        self.template_loader_stack.append(loader)
        self.update_template_env()

    def update_template_env(self):
        loaders = list(reversed(self.template_loader_stack))
        logger.debug(f"loaders: {loaders}")
        self.template_env = Environment(
            loader = ChoiceLoader(loaders),
            autoescape=select_autoescape()
        )