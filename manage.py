#!/usr/bin/env python
""" The main entry point for this app
"""
import logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'other': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'other',
        },
        'bare': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        '__main__': {
            'handlers': ['bare'],
            'level': 'INFO',
            'propagate': False
        },
    }
})
log = logging.getLogger(__name__)
log.info("Logging configured!")


if __name__ == '__main__':
    from commands import cli_app
    cli_app(obj={})
