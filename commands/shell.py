"""Drop into a Python REPL with application objects pre-imported
"""
import click

from app import create_app


def _create_context():
    """Returns a dictionary with application objects defined and
    configured
    """
    return {
        'app': create_app()
    }


@click.command()
@click.pass_context
def ipython(ctx):
    """ Run IPython REPL
    """
    try:
        import IPython
    except ImportError:
        click.secho('Cannot import IPython. Try `pip install IPython`')

    locals().update(_create_context())
    IPython.embed()
