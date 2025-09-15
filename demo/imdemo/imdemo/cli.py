from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import ImGuiDemo

__all__ = ["cli"]


def factory():
    app = ImGuiDemo().create()
    app.use_all()
    #app.show_channel("index")
    #app.show_channel("offscreen_canvas")
    #app.show_channel("offscreen_sprite")
    app.show_channel("offscreen_node")
    #app.show_channel("imagebutton")

    return app


set_demo_factory(factory)
