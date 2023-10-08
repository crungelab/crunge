import os
import importlib.util
from pathlib import Path

import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        update()


@cli.command()
@click.pass_context
def update(ctx):
    #print('update')
    global dot_procure
    path = Path(os.getcwd(), '.procure', '__init__.py')
    if os.path.exists(path):
        spec = importlib.util.spec_from_file_location(
            "dot_procure", path
        )
        dot_procure = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dot_procure)

    solutions = dot_procure.solutions

    for cls in solutions:
        solution = cls()
        print(f"Procuring:  {cls.__name__}")
        solution.update()
