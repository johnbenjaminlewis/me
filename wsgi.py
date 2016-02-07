from __future__ import absolute_import
from app import create_app


app = create_app(debug=False)


if __name__ == "__main__":
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
    app.run(host='0.0.0.0', debug=False)
