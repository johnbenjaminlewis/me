from nose.tools import assert_raises, eq_

from me.models import User
from . import utils


class TestUser(object):
    def setup(self):
        utils.clean_slate()

    def test_create(self):
        User(username='joe', name='joe').save()

        res = User.query.all()
        eq_(len(res), 1)
        eq_(res[0].username, 'joe')

        duplicate_user = User(username='joe', name='joe')
        assert_raises(Exception, lambda: duplicate_user.save())
