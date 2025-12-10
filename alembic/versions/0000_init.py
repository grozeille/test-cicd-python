"""create users table

Revision ID: 0000
Revises: 
Create Date: 2025-11-20 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import os

revision = '0000'
down_revision = None
branch_labels = None
depends_on = None

def _read_sql(name):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path = os.path.join(root, 'sql', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def upgrade() -> None:
    
    op.execute(_read_sql('0000_init.sql'))
    return


def downgrade() -> None:
    return
