import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TrackedTableMixin(object):
    date_created = sa.Column('date_created', sa.DateTime, nullable=False,
                             default=dt.datetime.utcnow)
    date_modified = sa.Column('date_modified', sa.DateTime, nullable=False,
                              default=dt.datetime.utcnow,
                              onupdate=dt.datetime.utcnow)


user_images = sa.Table(
        'user_images',
        Base.metadata,
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.user_id')),
        sa.Column('image_id', sa.BigInteger, sa.ForeignKey('images.image_id'))
)


class User(TrackedTableMixin, Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    username = sa.Column(sa.Text, unique=True, nullable=False)
    password_hash = sa.Column(sa.Text)
    password_salt = sa.Column(sa.Text)
    images = sa.orm.relationship('Image', secondary=user_images,
                                 back_populates='users')

    def __repr__(self):
        return '<{}(username="{}")>'.format(self.__class__.__name__,
                                            self.username)


class Image(TrackedTableMixin, Base):
    __tablename__ = 'images'
    image_id = sa.Column(sa.BigInteger, primary_key=True)
    cdn_url = sa.Column(sa.Text, nullable=False)
    users = sa.orm.relationship('User', secondary=user_images,
                                back_populates='images')

    def __repr__(self):
        return '<{}(username="{}")>'.format(self.__class__.__name__,
                                            self.cdn_url)
