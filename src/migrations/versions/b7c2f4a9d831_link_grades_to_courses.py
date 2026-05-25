"""link grades to courses

Revision ID: b7c2f4a9d831
Revises: a4d6f8b2c901
Create Date: 2026-05-25 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'b7c2f4a9d831'
down_revision: Union[str, Sequence[str], None] = 'a4d6f8b2c901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('grades', sa.Column('course_id', sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE grades
        SET course_id = assignments.course_id
        FROM assignments
        WHERE grades.assignment_id = assignments.id
        """
    )
    op.drop_constraint('grades_assignment_id_fkey', 'grades', type_='foreignkey')
    op.create_foreign_key(
        'grades_course_id_fkey',
        'grades',
        'courses',
        ['course_id'],
        ['id'],
    )
    op.alter_column('grades', 'course_id', nullable=False)
    op.drop_column('grades', 'assignment_id')


def downgrade() -> None:
    op.add_column('grades', sa.Column('assignment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'grades_assignment_id_fkey',
        'grades',
        'assignments',
        ['assignment_id'],
        ['id'],
    )
    op.drop_constraint('grades_course_id_fkey', 'grades', type_='foreignkey')
    op.drop_column('grades', 'course_id')
