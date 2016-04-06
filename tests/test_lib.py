from nose.tools import assert_raises, eq_, ok_

from me import lib


class TestConfig(object):

    def test_test_mode(self):
        conf = lib.Config()
        eq_(conf.has_initialized, False)
        assert_raises(RuntimeError, lambda: conf.something)
        conf.init()
        eq_(conf.has_initialized, True)
        eq_(conf.test_mode, True)
        assert_raises(AttributeError, lambda: conf.something)

    def test_prod_mode(self):
        conf = lib.Config()
        eq_(conf.has_initialized, False)
        assert_raises(RuntimeError, lambda: conf.something)
        conf.init(False)
        eq_(conf.has_initialized, True)
        eq_(conf.test_mode, False)
        assert_raises(AttributeError, lambda: conf.something)


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
