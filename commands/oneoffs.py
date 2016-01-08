# -*- coding: utf-8 -*-
""" Simple scripts or cron scripts that can get run
"""
import click

from .utils import include, write

NAME = 'oneoffs'
DOC = __doc__
COMMANDS = []


@include(COMMANDS)
@click.command()
@click.option('-d', default=1, help='this is help')
@click.pass_context
def cache_data(ctx, d):
    """ This is some subcommand
    """
    write("welcome to the command line ", fg='green')
