"""registration-approval

Revision ID: dc193136f858
Revises: bd25413d3ed5
Create Date: 2023-11-05 08:44:38.227358

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc193136f858"
down_revision: Union[str, None] = "bd25413d3ed5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    approvals = op.create_table(
        "registrationapprovaldb",
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),  # type: ignore
        sa.PrimaryKeyConstraint("email"),
    )
    # ### end Alembic commands ###

    op.bulk_insert(approvals, [{"email": "pfacko1@gmail.com"}])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("registrationapprovaldb")
    # ### end Alembic commands ###
