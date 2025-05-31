"""Initial migration

Revision ID: 7bc8e3b1f68c
Revises: 784042f80f3e
Create Date: 2025-05-31 11:35:16.691648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bc8e3b1f68c'
down_revision: Union[str, None] = '784042f80f3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch mode for SQLite compatibility
    with op.batch_alter_table('agents', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_agents_lisense_number', ['lisense_number'])

    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.alter_column(
            'description',
            existing_type=sa.VARCHAR(length=50),
            type_=sa.Text(),
            existing_nullable=True
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.alter_column(
            'description',
            existing_type=sa.Text(),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True
        )

    with op.batch_alter_table('agents', schema=None) as batch_op:
        batch_op.drop_constraint('uq_agents_lisense_number', type_='unique')
    # ### end Alembic commands ###
