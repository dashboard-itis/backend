"""add email notifications and account confirmation

Revision ID: 2e3fa99174f1
Revises: 9514f55d9f0d
Create Date: 2026-05-11 02:13:37.823444
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '2e3fa99174f1'
down_revision: Union[str, Sequence[str], None] = '9514f55d9f0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'is_confirmed',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    op.create_index(
        op.f('ix_users_is_confirmed'),
        'users',
        ['is_confirmed'],
        unique=False,
    )

    op.create_table(
        'email_notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_email_notifications_action'),
        'email_notifications',
        ['action'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_code'),
        'email_notifications',
        ['code'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_is_used'),
        'email_notifications',
        ['is_used'],
        unique=False,
    )
    op.create_index(
        op.f('ix_email_notifications_user_id'),
        'email_notifications',
        ['user_id'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_email_notifications_user_id'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_is_used'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_code'),
        table_name='email_notifications',
    )
    op.drop_index(
        op.f('ix_email_notifications_action'),
        table_name='email_notifications',
    )
    op.drop_table('email_notifications')

    op.drop_index(op.f('ix_users_is_confirmed'), table_name='users')
    op.drop_column('users', 'is_confirmed')
