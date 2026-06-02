"""make course stream and teacher nullable

Revision ID: c3d8e2a7b914
Revises: b7c2f4a9d831
Create Date: 2026-06-02 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = 'c3d8e2a7b914'
down_revision: Union[str, None] = 'b7c2f4a9d831'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'courses',
        'stream_id',
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.alter_column(
        'courses',
        'teacher_id',
        existing_type=sa.Integer(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'courses',
        'teacher_id',
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        'courses',
        'stream_id',
        existing_type=sa.Integer(),
        nullable=False,
    )
