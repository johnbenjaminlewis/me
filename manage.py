#!/usr/bin/env python
# TODO: port to Click
import IPython

from app import create_app


app = create_app()


if __name__ == '__main__':
    IPython.embed()
