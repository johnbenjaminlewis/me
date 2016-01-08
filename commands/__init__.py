# -*- coding: utf-8 -*-
"""This is the command line package. The main application is defined in
`commands/__init__.py`.

Individual modules can show up as separate CLI App arguments, grouping similar
functions together. More on this later...
"""
from __future__ import absolute_import
import click
from IPython import embed

# Modules to import as subgroups in the cli app
from . import oneoffs
from . import server
from .utils import write


menu_items = (
    oneoffs,
    server,
)


@click.group(help=__doc__)
@click.option('--test_mode', default=False, is_flag=True,
              help='Use test config')
@click.pass_context
def cli_app(ctx, test_mode):
    if test_mode:
        write('Using test mode', fg='green', err=True)
    else:
        write('Using production mode!', fg='yellow', err=True)


@click.command()
@click.pass_context
def shell(ctx):
    """ Run in IPython shell
    """
    from app import create_app
    app = create_app()
    embed()


# Register sub menu items
for item in menu_items:
    subgroup = click.Group(item.NAME, help=item.DOC)
    for command in item.COMMANDS:
        subgroup.add_command(command)

    cli_app.add_command(subgroup)


# Register additional commands
cli_app.add_command(shell)
