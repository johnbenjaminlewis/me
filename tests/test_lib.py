from nose.tools import assert_raises, eq_, ok_

from me import lib


def test_deep_merge():
    original = {'a': 1, 'b': 2}
    updates = {'b': 4}
    merged = lib.deep_merge(original, updates)
    eq_(merged['a'], 1)
    eq_(merged['b'], 4)

    original = {'a': 1, 'b': {'z': 'a', 'x': 'b'}}
    updates = {'b': {'z': 1}}
    merged = lib.deep_merge(original, updates)
    eq_(merged['a'], 1)
    eq_(merged['b']['z'], 1)
    eq_(merged['b']['x'], 'b')


def test_singleton():
    class A(object):
        __metaclass__ = lib.Singleton

    ok_(A() is A())


class TestConfig(object):
    def setup(self):
        self.config = lib.Config()

    def test_config(self):
        ok_(self.config.has_initialized is False)
        assert_raises(RuntimeError, lambda: self.config.settings)
        self.config.init()
        ok_(self.config.has_initialized)
        ok_(self.config.test_mode is True)
