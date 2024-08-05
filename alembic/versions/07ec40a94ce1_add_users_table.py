"""add users table

Revision ID: 07ec40a94ce1
Revises: 765ef87a1031
Create Date: 2024-08-05 19:44:37.207660

"""
from datetime import timezone
from re import S
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07ec40a94ce1'
down_revision: Union[str, None] = '765ef87a1031'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(),nullable=False),
                    sa.Column('email', sa.String(),nullable=False),
                    sa.Column('password', sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.text("now()") , nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass