# -*- coding: utf-8 -*-
""" Web server
"""
import click

from app import create_app


@click.command()
@click.option('--debug', '-d', default=True,
              help='Whether to run the app in debug mode')
@click.option('--hostname', '-h', default='0.0.0.0',
              help='The hostname to listen to')
@click.option('--port', '-p', default=5000,
              help='The port to bind to')
@click.pass_context
def run(ctx, hostname, port, debug):
    """ Run the web server
    """
    click.secho("Starting web server...\n", fg='green')
    create_app(debug=debug).run(host=hostname, port=port, debug=debug)
