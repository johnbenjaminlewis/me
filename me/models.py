import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TrackedTableMixin(object):
    date_created = sa.Column('date_created', sa.DateTime, nullable=False,
                             default=dt.datetime.utcnow)
    date_modified = sa.Column('date_modified', sa.DateTime, nullable=False,
                              default=dt.datetime.utcnow,
                              onupdate=dt.datetime.utcnow)


class User(TrackedTableMixin, Base):
    __tablename__ = 'users'

    user_id = sa.Column('user_id', sa.BigInteger, primary_key=True)
    name = sa.Column('name', sa.Text, nullable=False)
    username = sa.Column('username', sa.Text, unique=True, nullable=False)
    password_hash = sa.Column('password_hash', sa.Text)
    password_salt = sa.Column('password_salt', sa.Text)
