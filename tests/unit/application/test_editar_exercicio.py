import uuid

import pytest

from app.application.use_cases.editar_exercicio import EditarExercicio
from app.application.use_cases.exercicio_errors import (
    ExercicioNaoEncontradoError,
    ExercicioNomeDuplicadoError,
)
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class FakeExercicioRepository(ExercicioRepository):
    def __init__(self, exercicios: list[Exercicio]) -> None:
        self._exercicios = {e.id: e for e in exercicios}

    def get_by_id(self, exercicio_id):
        return self._exercicios.get(exercicio_id)

    def get_by_nome(self, nome):
        return next((e for e in self._exercicios.values() if e.nome.lower() == nome.lower()), None)

    def list_all(self, tipo=None):
        return list(self._exercicios.values())

    def add(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def update(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def delete(self, exercicio_id):
        self._exercicios.pop(exercicio_id, None)


def test_edita_exercicio_com_sucesso():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino]))

    editado = use_case.executar(supino.id, "Supino reto", TipoExercicio.MUSCULACAO)

    assert editado.nome == "Supino reto"


def test_editar_id_inexistente_falha():
    use_case = EditarExercicio(FakeExercicioRepository([]))

    with pytest.raises(ExercicioNaoEncontradoError):
        use_case.executar(uuid.uuid4(), "Supino", TipoExercicio.MUSCULACAO)


def test_editar_mantendo_proprio_nome_nao_conflita():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino]))

    editado = use_case.executar(supino.id, "Supino", TipoExercicio.MUSCULACAO)

    assert editado.nome == "Supino"


def test_editar_para_nome_de_outro_exercicio_falha():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    agachamento = Exercicio(id=uuid.uuid4(), nome="Agachamento", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino, agachamento]))

    with pytest.raises(ExercicioNomeDuplicadoError):
        use_case.executar(agachamento.id, "supino", TipoExercicio.MUSCULACAO)


def test_editar_com_nome_vazio_levanta_value_error():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino]))

    with pytest.raises(ValueError):
        use_case.executar(supino.id, "   ", TipoExercicio.MUSCULACAO)


def test_editar_com_nome_duplicado_de_outro_exercicio_levanta_erro():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    agachamento = Exercicio(id=uuid.uuid4(), nome="Agachamento", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino, agachamento]))

    with pytest.raises(ExercicioNomeDuplicadoError):
        use_case.executar(supino.id, "Agachamento", TipoExercicio.MUSCULACAO)


def test_editar_mantendo_o_proprio_nome_nao_levanta_duplicado():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    use_case = EditarExercicio(FakeExercicioRepository([supino]))

    resultado = use_case.executar(supino.id, "Supino", TipoExercicio.AEROBICO)

    assert resultado.tipo == TipoExercicio.AEROBICO
