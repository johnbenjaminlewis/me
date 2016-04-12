# -*- coding: utf-8 -*-
"""This is the command line package. The main application is defined in
`{this_file}`.

Individual modules can show up as separate CLI App arguments, grouping similar
functions together. More on this later...
"""
import logging
from importlib import import_module

import click

import me


MENU_GROUPS = (
    '.db',
    '.server',
    '.shell',
)


log = logging.getLogger(__name__)


def create_cli(menu_groups):
    """Similar to create_app, creates a click instance and returns it.

    :param menu_groups: a list of package names to import
    """
    @click.group(help=__doc__.format(this_file=__file__))
    @click.option('--test_mode', default=False, is_flag=True,
                  help='Use test config')
    @click.pass_context
    def cli_app(ctx, test_mode):
        if test_mode:
            click.secho('Using test mode', fg='green', err=True)
        else:
            click.secho('Using production mode!', fg='yellow', err=True)
        me.config.init(test_mode)

    # Import menu groups
    try:
        menu_groups = [import_module(g, package=__name__) for g in menu_groups]
    except ImportError as e:
        click.secho('Cannot import module "{}" from package "{}"'.format(
                    g, __name__), fg='red', bold=True)
        log.exception(e)
        raise SystemExit(1)

    # Register menu groups
    for group in menu_groups:
        group_name = group.__name__.split('.')[-1]
        group_doc = group.__doc__

        # Grab iterable of all objects defined in the module
        objects = group.__dict__.itervalues()
        commands = [o for o in objects if isinstance(o, click.Command)]
        if not commands:
            log.warn('No commands found in %s', group.__name__)

        subgroup = click.Group(group_name, help=group_doc)
        for command in commands:
            subgroup.add_command(command)

        cli_app.add_command(subgroup)

    return cli_app


cli_app = create_cli(MENU_GROUPS)
