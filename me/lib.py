from __future__ import absolute_import
import logging
import os.path

from cached_property import cached_property
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml


log = logging.getLogger(__name__)
DEFAULT_SETTINGS = 'me/etc/default.yaml'
OVERRIDE_SETTINGS = 'me/etc/override.yaml'


def _load_yaml(yaml_path):
    with open(yaml_path) as f:
        return yaml.load(f)


class Config(object):
    _pwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.realpath(os.path.join(_pwd, '..'))
    default_settings = _load_yaml(os.path.join(root_dir, DEFAULT_SETTINGS))
    override_settings = _load_yaml(os.path.join(root_dir, OVERRIDE_SETTINGS))

    def __init__(self):
        self.has_initialized = False
        self._settings = None

    def init(self, use_test_mode=True):
        self.test_mode = bool(use_test_mode)
        if self.has_initialized:
            log.warn('Cannot re-initialize config module')
            return
        settings = deep_merge(self.default_settings, self.override_settings)
        self.has_initialized = True
        log.info('Initializing Application...')
        self._settings = settings

    @cached_property
    def settings(self):
        if not self.has_initialized:
            raise RuntimeError('')
        return self._settings

    @property
    def main_db(self):
        engine = create_engine(URL(**self.settings['db']['primary']))
        Session = sessionmaker(bind=engine)
        return Session()


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
