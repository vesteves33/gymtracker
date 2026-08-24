import uuid

from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.infrastructure.db.repositories.exercicio_repository import (
    SqlAlchemyExercicioRepository,
)


def test_add_e_get_by_id(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    exercicio = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)

    repo.add(exercicio)
    encontrado = repo.get_by_id(exercicio.id)

    assert encontrado is not None
    assert encontrado.nome == "Supino"
    assert encontrado.tipo == TipoExercicio.MUSCULACAO


def test_get_by_id_retorna_none_se_nao_existir(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)

    assert repo.get_by_id(uuid.uuid4()) is None


def test_get_by_nome_e_case_insensitive(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    exercicio = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    assert repo.get_by_nome("SUPINO") is not None
    assert repo.get_by_nome("supino") is not None


def test_list_all_filtra_por_tipo(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    repo.add(Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO))
    repo.add(Exercicio(id=uuid.uuid4(), nome="Esteira", tipo=TipoExercicio.AEROBICO))

    resultado = repo.list_all(tipo=TipoExercicio.AEROBICO)

    assert [e.nome for e in resultado] == ["Esteira"]


def test_update_altera_nome_e_tipo(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    exercicio = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    repo.update(Exercicio(id=exercicio.id, nome="Supino reto", tipo=TipoExercicio.MUSCULACAO))

    atualizado = repo.get_by_id(exercicio.id)
    assert atualizado.nome == "Supino reto"


def test_delete_remove_exercicio(db_session):
    repo = SqlAlchemyExercicioRepository(db_session)
    exercicio = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    repo.add(exercicio)

    repo.delete(exercicio.id)

    assert repo.get_by_id(exercicio.id) is None
