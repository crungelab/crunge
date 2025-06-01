import click

from .demo import get_demo_factory


def create_demo():
    factory = get_demo_factory()
    return factory()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        demo = create_demo()
        demo.run()


@cli.command()
@click.pass_context
@click.argument("name")
def show(ctx, name):
    demo = create_demo()
    demo.show_channel(name)
    demo.run()
