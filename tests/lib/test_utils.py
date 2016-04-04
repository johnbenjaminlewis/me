from nose.tools import eq_, ok_

from me.lib import utils


def test_deep_merge():
    original = {'a': 1, 'b': 2}
    updates = {'b': 4}
    merged = utils.deep_merge(original, updates)
    eq_(merged['a'], 1)
    eq_(merged['b'], 4)

    original = {'a': 1, 'b': {'z': 'a', 'x': 'b'}}
    updates = {'b': {'z': 1}}
    merged = utils.deep_merge(original, updates)
    eq_(merged['a'], 1)
    eq_(merged['b']['z'], 1)
    eq_(merged['b']['x'], 'b')


def test_singleton():
    class A(object):
        __metaclass__ = utils.Singleton

    ok_(A() is A())
