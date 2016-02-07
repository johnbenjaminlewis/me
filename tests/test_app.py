from nose.tools import ok_

from app import create_app


class TestApp(object):
    @classmethod
    def setup_class(cls):
        cls.app = create_app(debug=False)
        cls.client = cls.app.test_client()

    def test_app(self):
        """ Verify we can GET homepage in prod mode
        """
        res = self.client.get('/')
        ok_(200 <= res.status_code < 300, res.status)
