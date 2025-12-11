from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import read_sql

revision = '0000'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute(read_sql('0000_init.sql'))
    return


def downgrade() -> None:
    op.execute(read_sql('0000_init_rollback.sql'))
    return
