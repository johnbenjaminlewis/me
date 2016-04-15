import click


def write(msg):
    return click.secho(msg, fg='cyan', err=True)
