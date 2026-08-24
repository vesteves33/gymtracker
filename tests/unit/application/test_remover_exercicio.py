import uuid

import pytest

from app.application.use_cases.exercicio_errors import ExercicioNaoEncontradoError
from app.application.use_cases.remover_exercicio import RemoverExercicio
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class FakeExercicioRepository(ExercicioRepository):
    def __init__(self, exercicios: list[Exercicio]) -> None:
        self._exercicios = {e.id: e for e in exercicios}

    def get_by_id(self, exercicio_id):
        return self._exercicios.get(exercicio_id)

    def get_by_nome(self, nome):
        return None

    def list_all(self, tipo=None):
        return list(self._exercicios.values())

    def add(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def update(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def delete(self, exercicio_id):
        self._exercicios.pop(exercicio_id, None)


def test_remove_exercicio_existente():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    repo = FakeExercicioRepository([supino])
    use_case = RemoverExercicio(repo)

    use_case.executar(supino.id)

    assert repo.get_by_id(supino.id) is None


def test_remover_id_inexistente_falha():
    use_case = RemoverExercicio(FakeExercicioRepository([]))

    with pytest.raises(ExercicioNaoEncontradoError):
        use_case.executar(uuid.uuid4())
