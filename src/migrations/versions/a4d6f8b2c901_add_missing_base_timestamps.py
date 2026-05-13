"""add missing base timestamps

Revision ID: a4d6f8b2c901
Revises: 2e3fa99174f1
Create Date: 2026-05-12 13:55:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'a4d6f8b2c901'
down_revision: Union[str, Sequence[str], None] = '2e3fa99174f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    timestamp = sa.DateTime()
    now = sa.text('now()')

    op.add_column(
        'groups',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'privacy_policies',
        sa.Column('created_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'streams',
        sa.Column('created_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'streams',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'users',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'courses',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'assignments',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'attendance',
        sa.Column('created_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'attendance',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'import_sources',
        sa.Column('created_at', timestamp, server_default=now, nullable=False),
    )
    op.add_column(
        'import_sources',
        sa.Column('updated_at', timestamp, server_default=now, nullable=False),
    )


def downgrade() -> None:
    op.drop_column('import_sources', 'updated_at')
    op.drop_column('import_sources', 'created_at')
    op.drop_column('attendance', 'updated_at')
    op.drop_column('attendance', 'created_at')
    op.drop_column('assignments', 'updated_at')
    op.drop_column('courses', 'updated_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('streams', 'updated_at')
    op.drop_column('streams', 'created_at')
    op.drop_column('privacy_policies', 'created_at')
    op.drop_column('groups', 'updated_at')
