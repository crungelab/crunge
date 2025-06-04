from pathlib import Path

from loguru import logger
import glm

from crunge.yoga import LayoutBuilder
from crunge import engine
from crunge.engine.resource.resource_manager import ResourceManager

from .page import Page
from .menubar import MenubarLocation


class Demo(engine.App):
    kWidth = 1280
    kHeight = 800

    def __init__(self, name: str, package_name: str, resource_root: Path):
        super().__init__(
            LayoutBuilder().width(self.kWidth).height(self.kHeight).build(),
            name,
            resizable=True,
        )
        self.package_name = package_name
        self.resource_root = resource_root
        ResourceManager().add_path_variables(
            resources=self.resource_root,
        )

        self.show_metrics = False
        self.show_style_editor = False
        self.menubar_location = MenubarLocation.WINDOW

    @property
    def page(self) -> Page:
        return self.view

    @page.setter
    def page(self, value: Page) -> None:
        self.view = value

    def use(self, name):
        logger.debug(f"using: {name}")
        import importlib.util

        spec = importlib.util.find_spec(f"{self.package_name}.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    def use_all(self, exclude: list = []):
        parent_folder = Path(self.package_name.replace(".", "/"), "pages")
        exclude = exclude + ["__pycache__", "__init__"]
        excluded = set(exclude)

        parent = Path(parent_folder)
        names = sorted([p.stem for p in parent.iterdir() if p.stem not in excluded])
        for name in names:
            self.use(name)


# The registry
DEMO_FACTORY = None


def set_demo_factory(fn):
    logger.debug(f"Setting demo factory: {fn}")
    global DEMO_FACTORY
    DEMO_FACTORY = fn


def get_demo_factory():
    logger.debug("Getting demo factory")
    if DEMO_FACTORY is None:
        raise RuntimeError("No Demo class registered!")
    return DEMO_FACTORY
