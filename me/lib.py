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
from sqlalchemy.orm import sessionmaker
import yaml


log = logging.getLogger(__name__)
config_log = logging.getLogger('.'.join((__name__.split('.')[0], 'config')))
Db = namedtuple('Db', ('Session', 'engine', 'session_manager'))


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


class Config(object):
    _pwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.realpath(os.path.join(_pwd, '..'))
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
            engine = create_engine(URL(**config[runtime_str]))
            # don't expire on commit, allowing the instantiated object to be
            # accessed without issuing a new DB query. If you want the updated
            # attrs, you need to manually query.
            Session = sessionmaker(bind=engine, expire_on_commit=False)
            db_attr = Db(Session, engine, session_manager_create(Session))
            setattr(self, db_name, db_attr)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


def deep_merge(base, updates):
    """ apply updates to base dictionary
    """
    for key, value in updates.iteritems():
        if key in base and isinstance(value, dict):
            base[key] = deep_merge(base[key] or {}, value)
        else:
            base[key] = value
    return base
