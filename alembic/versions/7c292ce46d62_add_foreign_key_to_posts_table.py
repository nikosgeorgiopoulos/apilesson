"""add foreign key to posts table

Revision ID: 7c292ce46d62
Revises: 07ec40a94ce1
Create Date: 2024-08-05 20:03:34.740489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c292ce46d62'
down_revision: Union[str, None] = '07ec40a94ce1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('creator_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table="posts", referent_table="users", local_cols=['creator_id'],remote_cols=[
        "id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
