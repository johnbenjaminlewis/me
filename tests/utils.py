""" Put testing utilities here
"""
import contextlib

from me import config
import me.models


def clean_slate():
    """ Truncates all tables
    """
    with contextlib.closing(config.main_db.engine.connect()) as con:
        trans = con.begin()
        for table in reversed(config.main_db.BaseModel.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
