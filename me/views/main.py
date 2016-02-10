# -*- coding: utf-8 -*-
from __future__ import absolute_import
import flask


blueprint = flask.Blueprint('main', __name__)
url_prefix = ''


@blueprint.route('/')
def index():
    return flask.render_template('index.j2')


@blueprint.route(u'/👋')
def hi():
    name = flask.request.args.get('name', 'Anonymous')
    return flask.render_template('hi.j2', name=name)
