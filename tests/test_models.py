from nose.tools import eq_

from me import config
from me.models import User
from . import utils


class TestUser(object):
    def setup(self):
        utils.clean_slate()

    def test_create(self):
        user = User(username='joe', name='joe')
        with config.main_db.session_manager() as s:
            s.add(user)

        with config.main_db.session_manager() as s:
            res = s.query(User).all()
            s.expunge(res[0])
        eq_(len(res), 1)
        eq_(res[0].username, 'joe')
