from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import LayoutDemo

__all__ = ["cli"]


def factory():
    app = LayoutDemo().create()
    app.use_all()
    app.show_channel("index")

    return app


set_demo_factory(factory)
