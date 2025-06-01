from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import ImPlotDemo

__all__ = ["cli"]


def factory():
    app = ImPlotDemo().create()
    app.use_all()
    app.show_channel("index")

    return app


set_demo_factory(factory)
