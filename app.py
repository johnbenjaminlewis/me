from __future__ import absolute_import
import logging

import flask

from views import BLUEPRINTS


log = logging.getLogger(__name__)


def create_app():
    log.info('Creating Flask app')
    app = flask.Flask(__name__)
    register_views(app)
    setup_jinja(app)
    return app


def register_views(app):
    for bp in BLUEPRINTS:
        log.info('Registering blueprint %s', bp.blueprint)
        app.register_blueprint(bp.blueprint, url_prefix=bp.url_prefix)


def setup_jinja(app):
    app.jinja_env.globals['site_name'] = 'JohnBenjaminLewis.com'
