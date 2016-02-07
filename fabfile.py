# -*- coding: utf-8 -*-
# Thanks @nficano (https://github.com/nficano)
from __future__ import absolute_import
from contextlib import contextmanager
from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import put
from fabric.api import run
from fabric.api import sudo

env.hosts = ['benlew.is']
# Use authentication information stored in `~/.ssh/config`.
env.use_ssh_config = True
# TODO: Replace hardcoded paths with setting variables.


@contextmanager
def virtualenv(name):
    """Handy context manager to activate a virtualenv.
    """
    with prefix('WORKON_HOME=$HOME/.virtualenvs'), \
         prefix('source /usr/local/bin/virtualenvwrapper.sh'), \
         prefix('workon {}'.format(name)):
                yield


def deploy():
    """Deploy updates to "production".
    """
    git_pull()
    pip_update()
    run_tests()
    restart_wsgi()


def git_pull():
    """Pull the latest version of the codebase.
    """
    with cd('~/repos/me'):
        run('git fetch origin && git reset --hard origin/master')


def restart_wsgi():
    """Gracefully restart wsgi.
    """
    sudo("restart benlew.is")


def pip_update():
    """Ensure all pip dependencies are up-to-date (or at least sync w/
    `requirements.txt`).
    """
    with virtualenv("benlew.is"):
        with cd('~/repos/me'):
            run("./install.sh")


def run_tests():
    """Run test suite.
    """
    with virtualenv("benlew.is"):
        with cd('~/repos/me'):
            run("nosetests")
