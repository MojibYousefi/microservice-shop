"""rename_hashed_password_to_password

Revision ID: 7c0ba638471e
Revises: 89f62bee9a9b
Create Date: 2026-08-24 23:13:12.303538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7c0ba638471e'
down_revision: Union[str, Sequence[str], None] = '89f62bee9a9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('hashed_password', new_column_name='password')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password', new_column_name='hashed_password')
