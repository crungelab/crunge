from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import ImFloDemo

__all__ = ["cli"]


def factory():
    app = ImFloDemo().create()
    app.use_all(exclude=['sparks'])
    app.show_channel("index")

    return app


set_demo_factory(factory)
