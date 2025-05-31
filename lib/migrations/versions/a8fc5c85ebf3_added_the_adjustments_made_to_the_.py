"""added the adjustments made to the columns

Revision ID: a8fc5c85ebf3
Revises: bd38311349f7
Create Date: 2025-05-31 21:54:46.985425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8fc5c85ebf3'
down_revision: Union[str, None] = 'bd38311349f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch_alter_table to safely alter constraints and columns in SQLite
    with op.batch_alter_table("agents") as batch_op:
        batch_op.drop_constraint("uq_agents_lisense_number", type_="unique")
        batch_op.drop_column("lisense_number")
        batch_op.add_column(sa.Column("license_number", sa.String(length=25), nullable=False))
        batch_op.create_unique_constraint("uq_agents_license_number", ["license_number"])

    with op.batch_alter_table("listings") as batch_op:
        batch_op.alter_column("address",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=100),
            existing_nullable=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("listings") as batch_op:
        batch_op.alter_column("address",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False
        )

    with op.batch_alter_table("agents") as batch_op:
        batch_op.drop_constraint(None, type_="unique")
        batch_op.drop_column("license_number")
        batch_op.add_column(sa.Column("lisense_number", sa.VARCHAR(length=25), nullable=False))
        batch_op.create_unique_constraint("uq_agents_lisense_number", ["lisense_number"])

