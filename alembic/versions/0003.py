from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('lastname', sa.String(length=255), nullable=True, unique=False),
    )



def downgrade() -> None:
    op.drop_column('users', 'lastname')
    return
