"""add last columns to posts table

Revision ID: 1b4803087ab5
Revises: 7c292ce46d62
Create Date: 2024-08-05 20:10:11.978603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b4803087ab5'
down_revision: Union[str, None] = '7c292ce46d62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('published', sa.Boolean(), nullable=False , server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False , server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
