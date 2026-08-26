"""seed exercicios

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-24 00:00:01.000000

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, Sequence[str], None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

EXERCICIOS_SEED = [
    ("Supino", "musculacao"),
    ("Agachamento", "musculacao"),
    ("Levantamento terra", "musculacao"),
    ("Remada", "musculacao"),
    ("Desenvolvimento de ombro", "musculacao"),
    ("Rosca direta", "musculacao"),
    ("Triceps pulley", "musculacao"),
    ("Esteira", "aerobico"),
    ("Bicicleta", "aerobico"),
    ("Escada", "aerobico"),
    ("Eliptico", "aerobico"),
]


def upgrade() -> None:
    connection = op.get_bind()
    for nome, tipo in EXERCICIOS_SEED:
        connection.execute(
            sa.text(
                "INSERT INTO exercicio (id, nome, tipo) VALUES (:id, :nome, :tipo) "
                "ON CONFLICT (nome) DO NOTHING"
            ),
            {"id": str(uuid.uuid4()), "nome": nome, "tipo": tipo},
        )


def downgrade() -> None:
    connection = op.get_bind()
    nomes = [nome for nome, _ in EXERCICIOS_SEED]
    connection.execute(
        sa.text("DELETE FROM exercicio WHERE nome = ANY(:nomes)"),
        {"nomes": nomes},
    )
