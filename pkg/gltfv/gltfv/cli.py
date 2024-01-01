import os
import importlib.util
from pathlib import Path

import click

from .build import build as _build

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

@cli.command()
@click.pass_context
def build(ctx):
    _build()
