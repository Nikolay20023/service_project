"""07

Revision ID: b781d7478758
Revises: d8a79b21b6c3
Create Date: 2024-02-10 21:07:40.084958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b781d7478758'
down_revision: Union[str, None] = 'd8a79b21b6c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_service', sa.Column('amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_service', 'amount')
    # ### end Alembic commands ###
