"""create users

Revision ID: bcb235a68ead
Revises:
Create Date: 2016-04-04 23:11:02.167001

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bcb235a68ead'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('username', sa.Text, unique=True, nullable=False),
        sa.Column('password_hash', sa.Text),
        sa.Column('password_salt', sa.Text),
        sa.Column('date_created', sa.DateTime, nullable=False,
                  server_default=sa.text('NOW()')),
        sa.Column('date_modified', sa.DateTime, nullable=False,
                  server_default=sa.text('NOW()'))
    )


def downgrade():
    op.drop_table('users')
