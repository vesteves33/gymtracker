import uuid

from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.infrastructure.db.repositories.exercicio_repository import (
    SqlAlchemyExercicioRepository,
)


def _nome_unico(base: str) -> str:
    return f"{base} Teste {uuid.uuid4().hex[:8]}"


def test_add_e_get_by_id(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    nome = _nome_unico("Supino")
    exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=TipoExercicio.MUSCULACAO)

    repo.add(exercicio)
    encontrado = repo.get_by_id(exercicio.id)

    assert encontrado is not None
    assert encontrado.nome == nome
    assert encontrado.tipo == TipoExercicio.MUSCULACAO


def test_get_by_id_retorna_none_se_nao_existir(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)

    assert repo.get_by_id(uuid.uuid4()) is None


def test_get_by_nome_e_case_insensitive(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    nome = _nome_unico("Supino")
    exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    assert repo.get_by_nome(nome.upper()) is not None
    assert repo.get_by_nome(nome.lower()) is not None


def test_list_all_filtra_por_tipo(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    nome_musc = _nome_unico("Supino")
    nome_aero = _nome_unico("Esteira")
    repo.add(Exercicio(id=uuid.uuid4(), nome=nome_musc, tipo=TipoExercicio.MUSCULACAO))
    repo.add(Exercicio(id=uuid.uuid4(), nome=nome_aero, tipo=TipoExercicio.AEROBICO))

    resultado = repo.list_all(tipo=TipoExercicio.AEROBICO)

    assert nome_aero in [e.nome for e in resultado]
    assert nome_musc not in [e.nome for e in resultado]


def test_update_altera_nome_e_tipo(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    nome = _nome_unico("Supino")
    nome_atualizado = _nome_unico("Supino reto")
    exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    repo.update(Exercicio(id=exercicio.id, nome=nome_atualizado, tipo=TipoExercicio.MUSCULACAO))

    atualizado = repo.get_by_id(exercicio.id)
    assert atualizado.nome == nome_atualizado


def test_delete_remove_exercicio(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    nome = _nome_unico("Supino")
    exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    repo.delete(exercicio.id)

    assert repo.get_by_id(exercicio.id) is None
