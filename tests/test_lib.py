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


def test_stentinel_int():
    for n in range(10):
        s = lib.SentinelInt(n)
        ok_(s != n)
        ok_(s != lib.SentinelInt(n))
        eq_(int(s), n)


def test_sorted_return():
    def gen_simple_list():
        return range(10)[::-1]

    def gen_list_of_dicts():
        return [{'a': n} for n in range(10)[::-1]]

    simple_list = lib.sorted_return(gen_simple_list)()
    eq_(range(10), simple_list)

    value_sort = lambda d: d['a']
    list_of_dicts = lib.sorted_return(key=value_sort)(gen_list_of_dicts)()
    eq_(range(10), [d['a'] for d in list_of_dicts])
