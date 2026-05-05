"""remove legacy user role enum

Revision ID: 9514f55d9f0d
Revises: 128564f80c46
Create Date: 2026-04-29
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = '9514f55d9f0d'
down_revision: Union[str, Sequence[str], None] = '128564f80c46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'role')


def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            postgresql.ENUM(
                'STUDENT',
                'CURATOR',
                'ADMIN',
                name='userrole',
                create_type=False,
            ),
            nullable=True,
        ),
    )
