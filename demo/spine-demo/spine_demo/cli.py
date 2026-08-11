from crunge.demo.cli import cli
from crunge.demo.demo import set_demo_factory
from .app import SpineDemo

__all__ = ["cli"]


def factory():
    app = SpineDemo().create()
    #app.use_all(exclude=['sparks'])
    app.use_all()
    app.show_channel("index")

    return app


set_demo_factory(factory)
