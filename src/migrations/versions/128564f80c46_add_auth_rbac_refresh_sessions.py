# ruff: noqa: E501

"""add auth rbac refresh sessions

Revision ID: 128564f80c46
Revises: 5b78cc8b5fbc
Create Date: 2026-04-29 01:20:39.725651
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '128564f80c46'
down_revision: Union[str, Sequence[str], None] = '5b78cc8b5fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column('subject', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('subject', 'action', name='uq_permissions_subject_action'),
    )
    op.create_index('ix_permissions_action', 'permissions', ['action'], unique=False)
    op.create_index('ix_permissions_subject', 'permissions', ['subject'], unique=False)

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_roles_name', 'roles', ['name'], unique=True)

    op.create_table(
        'role_permission_links',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    op.create_table(
        'refresh_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('access_token_jti', sa.String(length=100), nullable=False),
        sa.Column('refresh_token_jti', sa.String(length=100), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_invalidated', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_refresh_sessions_access_token_jti',
        'refresh_sessions',
        ['access_token_jti'],
        unique=True,
    )
    op.create_index(
        'ix_refresh_sessions_refresh_token_jti',
        'refresh_sessions',
        ['refresh_token_jti'],
        unique=True,
    )

    op.create_table(
        'user_role_links',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
    )


def downgrade() -> None:
    op.drop_table('user_role_links')

    op.drop_index(
        'ix_refresh_sessions_refresh_token_jti', table_name='refresh_sessions'
    )
    op.drop_index('ix_refresh_sessions_access_token_jti', table_name='refresh_sessions')
    op.drop_table('refresh_sessions')

    op.drop_table('role_permission_links')

    op.drop_index('ix_roles_name', table_name='roles')
    op.drop_table('roles')

    op.drop_index('ix_permissions_subject', table_name='permissions')
    op.drop_index('ix_permissions_action', table_name='permissions')
    op.drop_table('permissions')
