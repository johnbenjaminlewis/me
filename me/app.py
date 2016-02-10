from __future__ import absolute_import
import logging
import os

import flask
from flask.ext.assets import Bundle, Environment

from .views import BLUEPRINTS


log = logging.getLogger(__name__)


def create_app(debug=False):
    log.info('Creating Flask app')
    # Add custom access log
    logging.getLogger('werkzeug').addHandler(logging.FileHandler('access.log'))

    app = flask.Flask(__name__)
    register_node_bin(app.root_path)
    register_assets(app, debug)
    register_views(app)
    setup_jinja(app)
    return app


def register_node_bin(root_path):
    # TODO: This should get moved to a config module
    node_bin = os.path.join(root_path, 'node_modules', '.bin')
    if os.path.exists(node_bin):
        log.info('Adding local node binaries to system path')
        os.environ['PATH'] = ':'.join((node_bin, os.environ['PATH']))


def register_assets(app, debug=False):
    """We add the app's root path to assets search path. However, the
    output directory is relative to `app.static_folder`.
    """
    assets = Environment(app)
    assets.debug = debug
    assets.auto_build = True
    assets.manifest = 'file'
    assets.append_path(app.root_path)

    site_js = Bundle(
        'static_src/lib/jquery/jquery.js',
        'static_src/lib/bootstrap/js/dist/*.js',
        filters=('uglifyjs',),
        output='js/bundle.js'
    )
    assets.register('site_js', site_js)

    site_css = Bundle(
        'static_src/lib/bootstrap/dist/css/bootstrap.css',
        filters=('cssmin',),
        output='css/bundle.css'
    )
    assets.register('site_css', site_css)


def register_views(app):
    for bp in BLUEPRINTS:
        log.info('Registering blueprint "%s"', bp.blueprint.name)
        app.register_blueprint(bp.blueprint, url_prefix=bp.url_prefix)


def setup_jinja(app):
    app.jinja_env.globals['site_name'] = 'benlew.is'
