import importlib.util
import uuid
from pathlib import Path

from sqlalchemy import select, text

from app.infrastructure.db.models import ExercicioModel

_MIGRATION_PATH = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "infrastructure"
    / "db"
    / "migrations"
    / "versions"
    / "0003_seed_exercicios.py"
)


def _carregar_modulo_migration():
    spec = importlib.util.spec_from_file_location("migration_0003_seed_exercicios", _MIGRATION_PATH)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_seed_da_migration_0003_esta_presente_no_banco(db_session):
    modulo = _carregar_modulo_migration()

    for nome, tipo in modulo.EXERCICIOS_SEED:
        db_session.execute(
            text(
                "INSERT INTO exercicio (id, nome, tipo) VALUES (:id, :nome, :tipo) "
                "ON CONFLICT (nome) DO NOTHING"
            ),
            {"id": str(uuid.uuid4()), "nome": nome, "tipo": tipo},
        )
    db_session.commit()

    nomes_no_banco = {model.nome for model in db_session.execute(select(ExercicioModel)).scalars()}

    for nome, _tipo in modulo.EXERCICIOS_SEED:
        assert nome in nomes_no_banco


def test_seed_da_migration_0003_tem_tipos_validos(db_session):
    modulo = _carregar_modulo_migration()
    tipos_validos = {"musculacao", "aerobico"}

    for _nome, tipo in modulo.EXERCICIOS_SEED:
        assert tipo in tipos_validos
