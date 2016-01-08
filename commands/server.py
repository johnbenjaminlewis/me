# -*- coding: utf-8 -*-
""" Web server
"""
import click

from .utils import include, write
from app import create_app


NAME = 'server'
DOC = __doc__
COMMANDS = []


@include(COMMANDS)
@click.command()
@click.option('--hostname', '-h', default='0.0.0.0',
              help='The hostname to listen to')
@click.option('--port', '-p', default=5000,
              help='The port to bind to')
@click.pass_context
def run(ctx, hostname, port):
    """ This is some subcommand
    """
    write("Starting web server...\n", fg='green')
    create_app().run(host=hostname, port=port)
