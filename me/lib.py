""" Share classes, functions an utilities. Should not import app-specific
modules here.
"""
from __future__ import absolute_import
from collections import namedtuple
from contextlib import contextmanager
from functools import wraps
import logging
import os.path

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import yaml


log = logging.getLogger(__name__)
config_log = logging.getLogger('.'.join((__name__.split('.')[0], 'config')))


DEFAULT_SETTINGS = 'me/etc/default.yaml'
OVERRIDE_SETTINGS = 'me/etc/override.yaml'


def _load_yaml(yaml_path):
    with open(yaml_path) as f:
        return yaml.load(f)


def session_manager_create(Session):
    @contextmanager
    def session_manager(*args, **kwargs):
        session = Session(*args, **kwargs)
        try:
            yield session
            session.commit()
        except Exception as e:
            config_log.exception(e)
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()
    return session_manager


def _runonce(fn):
    @wraps(fn)
    def decorated(self, *args, **kwargs):
        if getattr(self, 'has_initialized', False):
            config_log.warn('Cannot re-initialize config module')
        else:
            return fn(self, *args, **kwargs)
    return decorated


class Db(object):
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        # don't expire on commit, allowing the instantiated object to be
        # accessed without issuing a new DB query. If you want the updated
        # attrs, you need to manually query.
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine,
                                                   expire_on_commit=False))
        self.session_manager = session_manager_create(self.session)

        def save_instance(instance):
            self.session.add(instance)
            try:
                self.session.commit()
            except Exception as e:
                config_log.exception(e)
                self.session.rollback()
                raise

        Base = declarative_base()
        Base.query = self.session.query_property()
        Base.save = save_instance
        self.BaseModel = Base


class Config(object):
    _pwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.realpath(os.path.join(_pwd, '..'))
    migrations_dir = os.path.join(root_dir, 'sql')

    default_settings = _load_yaml(os.path.join(root_dir, DEFAULT_SETTINGS))
    override_settings = _load_yaml(os.path.join(root_dir, OVERRIDE_SETTINGS))

    def __init__(self):
        self.has_initialized = False
        self._settings = None

    def __getattr__(self, name):
        if not self.has_initialized:
            raise RuntimeError('Cannot find property "{}". '
                               'Have you initialized'.format(name))
        return super(Config, self).__getattribute__(name)

    @_runonce
    def init(self, use_test_mode=True):
        self.test_mode = bool(use_test_mode)
        settings = deep_merge(self.default_settings, self.override_settings)
        self.has_initialized = True
        config_log.info('Initializing Application...')
        self.settings = settings
        self._setup_db()

    def _setup_db(self):
        runtime_str = 'test' if self.test_mode else 'prod'

        for db_name, config in self.settings['db'].iteritems():
            db_url = URL(**config[runtime_str])
            setattr(self, db_name, Db(db_url))


def deep_merge(base, updates):
    """ apply updates to base dictionary
    """
    for key, value in updates.iteritems():
        if key in base and isinstance(value, dict):
            base[key] = deep_merge(base[key] or {}, value)
        else:
            base[key] = value
    return base


class SentinelInt(int):
    """Makes unique sentinel values that look like integers but equality
    is overridden.
    """
    __slots__ = [e for e in dir(int) if not e.startswith('_')]

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self.__eq__(other) is False
