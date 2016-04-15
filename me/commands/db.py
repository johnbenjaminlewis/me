"""Any Database operations. E.g, upgrade, downgrade, etc
"""
import click

from me import config
from me import sql
from ._utils import write


@click.command()
@click.pass_context
def update(ctx):
    """ Runs migration script
    """
    updater = sql.DbUpdater(config.main_db, config.migrations_dir)
    if not updater.has_bootstrapped:
        write('Bootrapping SQL...')
        updater.bootstrap()
    else:
        write('SQL already bootstrapped')

    new_migrations = [m for m in updater.migrations
                      if m > updater.current_version]
    if new_migrations:
        write('Found {} new migrations'.format(len(new_migrations)))
        for migration in new_migrations:
            updater.run_migration(migration)
    else:
        write('No new migrations')

    ctx.invoke(grant)


@click.command()
@click.pass_context
def grant(ctx):
    write('Granting permissions to database engines')
    updater = sql.DbUpdater(config.main_db, config.migrations_dir)
    updater.grant_all_users()
