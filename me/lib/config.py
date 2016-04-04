import logging
import os.path

import yaml


log = logging.getLogger(__name__)


class Config(object):
    __name__ = __name__
    _yaml = yaml

    _pwd = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.realpath(os.path.join(_pwd, '..', '..'))
    app_dir = os.path.join(root_dir, 'me')

    def __init__(self):
        self.has_initialized = False
        self.hello_monster = 'Hi'

    def init(self, use_test_mode=True):
        self.test_mode = bool(use_test_mode)
        if self.has_initialized:
            log.warn('Cannot re-initialize config module')
            return
        with open(os.path.join(self.app_dir, 'etc', 'default.yaml')) as f:
            settings = yaml.load(f)
        self._init(settings)

    def _init(self, settings):
        self.has_initialized = True
        log.info('Initializing Application...')
        self.settings = settings

    def __getattr__(self, name):
        msg = 'No attribute "{}". Have you initialized?'.format(name)
        raise AttributeError(msg)
