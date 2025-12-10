"""create users table

Revision ID: 0003
Revises: 
Create Date: ***
"""
from alembic import op
import sqlalchemy as sa
import os

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('lastname', sa.String(length=255), nullable=True, unique=False),
        sa.Column('middlename', sa.String(length=255), nullable=True, unique=False)
    )



def downgrade() -> None:
    # TODO
    return
