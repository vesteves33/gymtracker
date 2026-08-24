"""create exercicio

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-24 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exercicio',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
        sa.CheckConstraint("tipo IN ('musculacao', 'aerobico')", name='ck_exercicio_tipo'),
    )


def downgrade() -> None:
    op.drop_table('exercicio')
