from __future__ import absolute_import
from collections import namedtuple


from . import main


BlueprintInfo = namedtuple('BlueprintInfo', ('blueprint', 'url_prefix'))


BLUEPRINTS = [
    BlueprintInfo(main.blueprint, main.url_prefix)
]
