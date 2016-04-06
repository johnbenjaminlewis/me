""" Put testing utilities here
"""
import contextlib

from me.models import Base

from me import config


def clean_slate():
    """ Truncates all tables
    """
    with contextlib.closing(config.main_db.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
