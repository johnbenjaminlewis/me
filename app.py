from __future__ import absolute_import
import logging

import flask
from flask.ext.assets import Bundle, Environment

from views import BLUEPRINTS


log = logging.getLogger(__name__)


def create_app(debug=False):
    log.info('Creating Flask app')
    # Add custom access log
    logging.getLogger('werkzeug').addHandler(logging.FileHandler('access.log'))

    app = flask.Flask(__name__)
    register_assets(app, debug)
    register_views(app)
    setup_jinja(app)
    return app


def register_assets(app, debug=False):
    """We add the app's root path to assets search path. However, the
    output directory is relative to `app.static_folder`.
    """
    assets = Environment(app)
    assets.debug = debug
    assets.auto_build = debug
    assets.manifest = 'file'
    assets.append_path(app.root_path)

    site_js = Bundle(
        'static_src/lib/jquery/jquery.js',
        'static_src/lib/bootstrap/js/dist/*.js',
        filters=('uglifyjs',),
        output='js/bundle.$(version)s.js'
    )
    assets.register('site_js', site_js)

    site_css = Bundle(
        'static_src/lib/bootstrap/dist/css/bootstrap.css',
        filters=('cssmin',),
        output='css/bundle.$(version)s.css'
    )
    assets.register('site_css', site_css)


def register_views(app):
    for bp in BLUEPRINTS:
        log.info('Registering blueprint %s', bp.blueprint)
        app.register_blueprint(bp.blueprint, url_prefix=bp.url_prefix)


def setup_jinja(app):
    app.jinja_env.globals['site_name'] = 'benlew.is'
