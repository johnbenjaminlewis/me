from nose.tools import assert_raises, ok_

from me.lib import config


class TestConfig(object):
    def setup(self):
        self.config = config.Config()

    def test_config(self):
        ok_(self.config.has_initialized is False)
        assert_raises(AttributeError, lambda: config.settings)
        self.config.init()
        ok_(self.config.has_initialized)
        ok_(self.config.test_mode is True)
