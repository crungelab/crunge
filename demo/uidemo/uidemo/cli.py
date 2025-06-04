from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import UiDemo

__all__ = ["cli"]


def factory():
    app = UiDemo().create()
    app.use_all()
    app.show_channel("index")

    return app


set_demo_factory(factory)
