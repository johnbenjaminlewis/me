# -*- coding: utf-8 -*-
""" Web server
"""
import logging
import click

from me.app import create_app


log = logging.getLogger(__name__)


@click.command()
@click.option('--debug', '-d', is_flag=True,
              help='Whether to run the app in debug mode')
@click.option('--hostname', '-h', default='0.0.0.0',
              help='The hostname to listen to')
@click.option('--port', '-p', default=5000,
              help='The port to bind to')
@click.pass_context
def run(ctx, hostname, port, debug):
    """ Run the web server
    """
    log.info('Debug is %s', debug)
    click.secho("Starting web server...\n", fg='green')
    create_app(debug=debug).run(host=hostname, port=port, debug=debug)
