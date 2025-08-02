from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import ImGuiDemo

__all__ = ["cli"]


def factory():
    app = ImGuiDemo().create()
    app.use_all()
    #app.show_channel("index")
    app.show_channel("offscreen")

    return app


set_demo_factory(factory)
