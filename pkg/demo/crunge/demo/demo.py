from pathlib import Path
from typing import Callable

from loguru import logger

from crunge import imgui
from crunge import engine
from crunge.engine.resource.resource_manager import ResourceManager

from .page import Page
from .menubar import MenubarLocation

first_time = True

class Demo(engine.App):
    def __init__(self, title: str, package_name: str, resource_root: Path):
        super().__init__(
            title=title,
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

        self.fullwidth = True
        self.fullheight = True

    @property
    def page(self) -> Page:
        return self.display

    @page.setter
    def page(self, value: Page) -> None:
        self.display = value

    def use(self, name):
        logger.debug(f"using: {name}")
        import importlib.util

        spec = importlib.util.find_spec(f"{self.package_name}.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    def use_all(self, exclude: list[str] = []):
        import importlib.util

        pages_package = f"{self.package_name}.pages"
        spec = importlib.util.find_spec(pages_package)
        if spec is None:
            raise ImportError(f"Cannot find package: {pages_package}")

        # Resolve the actual filesystem path of the pages package
        parent = Path(spec.submodule_search_locations[0])

        exclude = exclude + ["__pycache__", "__init__"]
        excluded = set(exclude)

        names = sorted([p.stem for p in parent.iterdir() if p.stem not in excluded])
        for name in names:
            self.use(name)


    def _draw(self):
        self.draw_main_dockspace()

        if self.show_metrics:
            self.show_metrics = imgui.show_metrics_window(True)

        if self.show_style_editor:
            self.show_style_editor = imgui.begin("Style Editor", True)[1]
            imgui.show_style_editor()
            imgui.end()

        if self.menubar_location == MenubarLocation.WINDOW:
            self.draw_mainmenu()
        self.draw_navbar()

        if self.fullwidth:
            x = self.width - (512 + 256) - 32
            width = 512
        else:
            x = self.width - (512) - 32
            width = 512 / 2

        if self.fullheight:
            y = 32
            height = self.height - 32 - 16
        else:
            y = 32
            height = (self.height - 32 - 16) / 2

        #imgui.set_next_window_pos((x, y), imgui.Cond.ONCE)
        #imgui.set_next_window_size((width, height), imgui.Cond.ONCE)

        super()._draw()

    def draw_main_dockspace(self):
        dockspace_id = imgui.get_id("MainDockspace")
        vp = imgui.get_main_viewport()

        if imgui.internal.dock_builder_get_node(dockspace_id) is None:
            imgui.internal.dock_builder_add_node(
                dockspace_id, imgui.internal.DockNodeFlags.DOCK_SPACE
            )
            imgui.internal.dock_builder_set_node_size(dockspace_id, vp.work_size)

            dock_right, _ = imgui.internal.dock_builder_split_node(
                dockspace_id, imgui.Dir.RIGHT, 0.22
            )
            dock_right_bottom, dock_right_top = imgui.internal.dock_builder_split_node(
                dock_right, imgui.Dir.DOWN, 0.45
            )

            imgui.internal.dock_builder_dock_window("Examples", dock_right_top)
            imgui.internal.dock_builder_dock_window("Properties", dock_right_bottom)
            imgui.internal.dock_builder_finish(dockspace_id)

        imgui.dock_space_over_viewport(
            dockspace_id, vp, imgui.DockNodeFlags.PASSTHRU_CENTRAL_NODE
        )

    '''
    def draw_main_dockspace(self):
        dockspace_id = imgui.get_id("MainDockspace")
        vp = imgui.get_main_viewport()

        if imgui.internal.dock_builder_get_node(dockspace_id) is None:
            imgui.internal.dock_builder_add_node(
                dockspace_id, imgui.internal.DockNodeFlags.DOCK_SPACE
            )
            imgui.internal.dock_builder_set_node_size(dockspace_id, vp.work_size)

            dock_left, dock_center = imgui.internal.dock_builder_split_node(
                dockspace_id, imgui.Dir.LEFT, 0.25
            )
            imgui.internal.dock_builder_dock_window("Examples", dock_left)
            imgui.internal.dock_builder_finish(dockspace_id)

        imgui.dock_space_over_viewport(
            dockspace_id, vp, imgui.DockNodeFlags.PASSTHRU_CENTRAL_NODE
        )
    '''

    def draw_navbar(self):
        flags = imgui.WindowFlags.MENU_BAR if self.menubar_location == MenubarLocation.NAVBAR else imgui.WindowFlags.NONE
        imgui.begin("Examples", flags=flags)

        if self.menubar_location == MenubarLocation.NAVBAR:
            if imgui.begin_menu_bar():
                self.draw_menu_bar()
                imgui.end_menu_bar()

        if imgui.begin_list_box(f"##Examples", (-1, -1)):

            for channel in self.channels.values():
                opened, selected = imgui.selectable(
                    channel.title, channel.name == self.channel.name
                )
                if opened:
                    self.show_channel(channel.name)

            imgui.end_list_box()

        imgui.end()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            self.draw_menu_bar()
            imgui.end_main_menu_bar()

    def draw_menu_bar(self):
        if imgui.begin_menu("File", True):
            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", "Cmd+Q", False, True
            )

            if clicked_quit:
                exit(1)

            imgui.end_menu()
        # View
        if imgui.begin_menu("View", True):
            clicked_metrics, self.show_metrics = imgui.menu_item(
                "Metrics", "Cmd+M", self.show_metrics, True
            )
            clicked_metrics, self.show_style_editor = imgui.menu_item(
                "Style Editor", "Cmd+S", self.show_style_editor, True
            )
            imgui.end_menu()
# The registry
DEMO_FACTORY = None


def set_demo_factory(fn: Callable[[], Demo]):
    logger.debug(f"Setting demo factory: {fn}")
    global DEMO_FACTORY
    DEMO_FACTORY = fn


def get_demo_factory() -> Callable[[], Demo]:
    logger.debug("Getting demo factory")
    if DEMO_FACTORY is None:
        raise RuntimeError("No Demo class registered!")
    return DEMO_FACTORY