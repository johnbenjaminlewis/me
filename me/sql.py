import collections
import functools
import logging
import os
import re

import sqlalchemy as sa

from me import lib


BOOTSTRAP_FILE = 'bootstrap.sql'
NO_VERSION = lib.SentinelInt(-1)
SQL_VERSION_REGEX = re.compile(r'^\d+')
SQL_PERM_REGEX = re.compile(r'^[\w\s]+$')
log = logging.getLogger(__name__)


def _sorted_query(key):
    def decorator(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            res = fn(*args, **kwargs)
            return sorted(res, key=key)
        return decorated
    return decorator


def get_sql_version(filename):
    try:
        assert filename.endswith('.sql')
        res = SQL_VERSION_REGEX.match(filename)
        return int(res.group())
    except AssertionError:
        raise ValueError('{} does not have ".sql" '
                         'file extension'.format(filename))
    except (AttributeError, TypeError):
        raise ValueError('Invalid version chunk at '
                         'beginning of filename {}'.format(filename))


class Migration(int):
    """ So we can compare db migration verisions like ints
    """
    def __new__(cls, filename, version):
        obj = int.__new__(cls, version)
        obj.filename = filename
        obj.version = version
        return obj

    def __repr__(self):
        return '<Migration {}: "{}">'.format(self.version, self.filename)


class DbUpdater(object):
    def __init__(self, db, migrations_dir):
        self.db = db
        self.meta = sa.MetaData(bind=db.engines['migration'])
        self.migrations_dir = migrations_dir

    @property
    def versions(self):
        return sa.Table('versions', self.meta, autoload=True)

    @property
    @lib.sorted_return
    def migrations(self):
        """Grab all versioned migrations from the migration directory, verify
        no duplicates and return list.
        """
        files = os.listdir(self.migrations_dir)
        migrations = []
        for _file in files:
            try:
                version = get_sql_version(_file)
            except ValueError:
                # Skip invlaid sql migration version
                continue
            migrations.append(Migration(_file, version))
        counts = collections.Counter(m.version for m in migrations).iteritems()
        dupes = sorted(v for v, count in counts if count > 1)
        if dupes:
            msg = 'Duplicate migration detected: versions {}'.format(dupes)
            raise SystemExit(msg)
        return migrations

    @property
    @lib.sorted_return(key=lambda e: e.tablename)
    def tables(self):
        """ Returns list of non-meta postgres tables.
        """
        return self._query_nonsystem_objects('pg_tables')

    @property
    @lib.sorted_return(key=lambda e: e.viewname)
    def views(self):
        """ Returns list of non-meta postgres views.
        """
        return self._query_nonsystem_objects('pg_views')

    @property
    @lib.sorted_return(key=lambda e: e.matviewname)
    def matviews(self):
        """ Returns list of non-meta postgres materialized views.
        """
        return self._query_nonsystem_objects('pg_matviews')

    @property
    @lib.sorted_return(key=lambda e: e.sequence_name)
    def sequences(self):
        """ Returns list of postgres sequences.
        """
        pg_table = sa.Table('sequences', self.meta, autoload=True,
                            schema='information_schema')
        with self.db.session_manager() as s:
            return s.query(pg_table).all()

    @property
    @lib.sorted_return(key=lambda e: e.schema_name)
    def schemata(self):
        """ Returns list of postgres schemata.
        """
        pg_table = sa.Table('schemata', self.meta, autoload=True,
                            schema='information_schema')
        with self.db.session_manager() as s:
            return s.query(pg_table)\
                    .filter(~pg_table.c.schema_name.match('pg_%'))\
                    .filter(pg_table.c.schema_name != 'information_schema')\
                    .all()

    @property
    def users(self):
        """ Returns list of postgres users.
        """
        pg_table = sa.Table('pg_user', self.meta, autoload=True,
                            schema='pg_catalog')
        with self.db.session_manager() as s:
            return s.query(pg_table).all()

    @property
    def has_bootstrapped(self):
        return self.current_version != NO_VERSION

    @property
    def current_version(self):
        if any('versions' in table.tablename for table in self.tables):
            with self.db.session_manager() as s:
                return s.query(sa.func.max(self.versions.c.to_version))\
                        .scalar() or 0
        return NO_VERSION

    def _query_nonsystem_objects(self, table_name):
        pg_table = sa.Table(table_name, self.meta, autoload=True,
                            schema='pg_catalog')
        with self.db.session_manager() as s:
            return s.query(pg_table)\
                    .filter(pg_table.c.schemaname != 'pg_catalog')\
                    .filter(pg_table.c.schemaname != 'information_schema')\
                    .all()

    def bootstrap(self):
        boostrap_migration = Migration(BOOTSTRAP_FILE, 0)
        self.run_migration(boostrap_migration)

    def run_migration(self, migration):
        log.info('Running %r', migration)
        with open(os.path.join(self.migrations_dir, migration.filename)) as f:
            with self.db.session_manager() as s:
                # Update schema, write changes then bump version
                s.execute(f.read())
                s.commit()
                s.execute(self.versions.insert()
                              .values(from_version=self.current_version,
                                      to_version=migration.version))

    def grant_permissions(self, permission, object_name, user, schema=None):
        """ Grants privilege to user.

        :raises AssertionError: if invalid permission, object, user,
                                or schema.
        """
        allowed_permissions = ('ALL', 'SELECT', 'UPDATE', 'USAGE')
        allowed_schemata = [s.schema_name for s in self.schemata]
        allowed_users = [u.usename for u in self.users]

        if isinstance(permission, basestring):
            permission = [permission]
        # We have to use regular python string interpolation for dynamic sql
        assert (all(p in allowed_permissions for p in permission)), (
                'Invalid permision {}'.format(permission))
        if schema:
            assert (schema in allowed_schemata), (
                    'Invalid schema {}'.format(schema))
        assert user in allowed_users, 'Invalid user {}'.format(user)
        assert (SQL_PERM_REGEX.match(object_name) is not None), (
                'Invalid object name {}'.format(object_name))

        permission = ', '.join(permission)

        if schema:
            on_clause = '{}.{}'.format(schema, object_name)
        else:
            on_clause = object_name

        statement = "GRANT {} ON {} TO {}".format(permission, on_clause, user)

        log.info('Granting "%s" on "%s" to %s', permission, on_clause, user)
        with self.db.session_manager() as s:
            s.execute(statement)

    def grant_all_users(self):
        for engine_name, engine in self.db.engines.iteritems():
            if engine_name == 'migration':
                # Migration engine already has permissions
                continue
            log.info('Processing permissions for "%s" engine', engine_name)

            user = engine.url.username

            # Set different permissions to grant
            if engine_name == 'write':
                object_permissions = 'ALL'
                sequence_permissions = 'ALL'
                schema_permissions = 'USAGE'
            else:
                object_permissions = 'SELECT'
                sequence_permissions = ['SELECT', 'UPDATE']
                schema_permissions = 'USAGE'

            # Grant for each type of object
            for table in self.tables:
                self.grant_permissions(object_permissions, table.tablename,
                                       user, schema=table.schemaname)
            for view in self.views:
                self.grant_permissions(object_permissions, view.viewname,
                                       user, schema=view.schemaname)
            for matview in self.matviews:
                self.grant_permissions(object_permissions, matview.matviewname,
                                       user, schema=matview.schemaname)
            for sequence in self.sequences:
                self.grant_permissions(sequence_permissions,
                                       sequence.sequence_name,
                                       user, schema=sequence.sequence_schema)
            for schema in self.schemata:
                self.grant_permissions(schema_permissions,
                                       'SCHEMA {}'.format(schema.schema_name),
                                       user)
