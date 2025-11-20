"""create users table

Revision ID: 0001
Revises: 
Create Date: 2025-11-20 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import os

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def _read_sql(name):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path = os.path.join(root, 'sql', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('last_logon', sa.DateTime(), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False),
    )

    op.execute(_read_sql('0001_create_users.sql'))


def downgrade() -> None:
    op.drop_table('users')
