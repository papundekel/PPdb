"""profiles

Revision ID: 5bcf65a89a6d
Revises: dc193136f858
Create Date: 2023-11-06 10:04:43.663120

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5bcf65a89a6d"
down_revision: Union[str, None] = "dc193136f858"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "profiledb",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "profileaccessdb",
        sa.Column(
            "access",
            sa.Enum("read", "write", "own", name="profileaccesstype"),
            nullable=False,
        ),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiledb.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["profiledb.id"],
        ),
        sa.PrimaryKeyConstraint("profile_id", "user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("profileaccessdb")
    op.drop_table("profiledb")
    # ### end Alembic commands ###
