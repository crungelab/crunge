import cProfile
import pstats

import click

from .wrender import WRender


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        WRender().run()

@cli.command()
@click.pass_context
def profile(ctx):
    profiler = cProfile.Profile()
    profiler.enable()

    WRender().run()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('time').print_stats(10)

    profiler.dump_stats('wrender.prof')
