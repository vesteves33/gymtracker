import uuid

import pytest

from app.application.use_cases.criar_exercicio import CriarExercicio
from app.application.use_cases.exercicio_errors import ExercicioNomeDuplicadoError
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class FakeExercicioRepository(ExercicioRepository):
    def __init__(self, exercicios: list[Exercicio] | None = None) -> None:
        self._exercicios = {e.id: e for e in (exercicios or [])}

    def get_by_id(self, exercicio_id: uuid.UUID) -> Exercicio | None:
        return self._exercicios.get(exercicio_id)

    def get_by_nome(self, nome: str) -> Exercicio | None:
        for exercicio in self._exercicios.values():
            if exercicio.nome.lower() == nome.lower():
                return exercicio
        return None

    def list_all(self, tipo: TipoExercicio | None = None) -> list[Exercicio]:
        valores = list(self._exercicios.values())
        if tipo is not None:
            valores = [e for e in valores if e.tipo == tipo]
        return valores

    def add(self, exercicio: Exercicio) -> None:
        self._exercicios[exercicio.id] = exercicio

    def update(self, exercicio: Exercicio) -> None:
        self._exercicios[exercicio.id] = exercicio

    def delete(self, exercicio_id: uuid.UUID) -> None:
        self._exercicios.pop(exercicio_id, None)


def test_cria_exercicio_com_sucesso():
    use_case = CriarExercicio(FakeExercicioRepository())

    exercicio = use_case.executar("Supino", TipoExercicio.MUSCULACAO)

    assert exercicio.nome == "Supino"
    assert exercicio.tipo == TipoExercicio.MUSCULACAO


def test_recusa_nome_vazio():
    use_case = CriarExercicio(FakeExercicioRepository())

    with pytest.raises(ValueError):
        use_case.executar("   ", TipoExercicio.MUSCULACAO)


def test_recusa_nome_duplicado_case_insensitive():
    existente = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    use_case = CriarExercicio(FakeExercicioRepository([existente]))

    with pytest.raises(ExercicioNomeDuplicadoError):
        use_case.executar("supino", TipoExercicio.MUSCULACAO)
