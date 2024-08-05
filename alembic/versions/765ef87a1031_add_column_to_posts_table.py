"""add column to posts table

Revision ID: 765ef87a1031
Revises: b8817f19b759
Create Date: 2024-08-05 19:44:26.878572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '765ef87a1031'
down_revision: Union[str, None] = 'b8817f19b759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
