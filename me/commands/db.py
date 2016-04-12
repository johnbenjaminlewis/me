"""Any Database operations. E.g, upgrade, downgrade, etc
"""
import click


@click.command()
@click.pass_context
def update(ctx):
    """ Runs migration script
    """
    import IPython;IPython.embed()
