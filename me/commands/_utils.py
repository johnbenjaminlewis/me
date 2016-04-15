import click


def write(msg):
    return click.secho(msg, fg='cyan', err=True)


def fail(msg):
    click.secho(msg, fg='red', err=True)
    raise SystemExit(1)
