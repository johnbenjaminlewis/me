""" Put testing utilities here
"""
from me import config


def clean_slate():
    """ Truncates all tables
    """
    db = config.main_db
    with db.session_manager(bind=db.engines['migration']) as s:
        for table in reversed(config.main_db.BaseModel.metadata.sorted_tables):
            s.execute(table.delete())
