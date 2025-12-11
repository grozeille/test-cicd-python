from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import read_sql

revision = '0001'
down_revision = '0000'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('price', sa.Float(), nullable=True),
    )
    op.execute(read_sql('0001_create_products.sql'))


def downgrade() -> None:
    op.drop_table('products')
