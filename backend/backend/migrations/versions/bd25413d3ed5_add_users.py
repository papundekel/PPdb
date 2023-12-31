"""add-users

Revision ID: bd25413d3ed5
Revises: f11c23a7c5b5
Create Date: 2023-11-03 21:17:54.561081

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bd25413d3ed5"
down_revision: Union[str, None] = "f11c23a7c5b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userdb",
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "tokendb",
        sa.Column("token", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["userdb.id"],
        ),
        sa.PrimaryKeyConstraint("token"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tokendb")
    op.drop_table("userdb")
    # ### end Alembic commands ###
