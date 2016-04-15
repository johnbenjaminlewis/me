"""Any Database operations. E.g, upgrade, grant, rebuid test, etc.
"""
from subprocess import call

import click

from me import config
from me import sql
from ._utils import write, fail


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
    """ Grants permissions to read and write database users
    """
    write('Granting permissions to database engines')
    updater = sql.DbUpdater(config.main_db, config.migrations_dir)
    updater.grant_all_users()


@click.command()
@click.pass_context
def rebuild(ctx):
    """ Completely rebuilds test db. Can only be used with --test-mode flag
    """
    if not config.test_mode:
        return fail('rebuild may only be used in test mode! Aborting.')
    write('Rebuilding test database')
    updater = sql.DbUpdater(config.main_db, config.migrations_dir)
    engine = updater.db.engines['migration']
    user = engine.url.username
    database = engine.url.database

    # Begin calls

    res = call(['dropdb', database, '-U', user])
    if res:
        return fail('Drop db operation failed!')
    res = call(['createdb', database, '-E', 'utf8', '-l', 'en_US.utf8',
                '-T', 'template0', '-U', user])
    if res:
        return fail('createdb operation failed!')
    write('Test database {} rebuilt successfully'.format(database))
    ctx.invoke(grant)
