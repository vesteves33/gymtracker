import uuid

from app.application.use_cases.listar_exercicios import ListarExercicios
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class FakeExercicioRepository(ExercicioRepository):
    def __init__(self, exercicios: list[Exercicio]) -> None:
        self._exercicios = {e.id: e for e in exercicios}

    def get_by_id(self, exercicio_id):
        return self._exercicios.get(exercicio_id)

    def get_by_nome(self, nome):
        return next((e for e in self._exercicios.values() if e.nome.lower() == nome.lower()), None)

    def list_all(self, tipo: TipoExercicio | None = None) -> list[Exercicio]:
        valores = list(self._exercicios.values())
        if tipo is not None:
            valores = [e for e in valores if e.tipo == tipo]
        return valores

    def add(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def update(self, exercicio):
        self._exercicios[exercicio.id] = exercicio

    def delete(self, exercicio_id):
        self._exercicios.pop(exercicio_id, None)


def test_lista_todos_sem_filtro():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    esteira = Exercicio(id=uuid.uuid4(), nome="Esteira", tipo=TipoExercicio.AEROBICO)
    use_case = ListarExercicios(FakeExercicioRepository([supino, esteira]))

    resultado = use_case.executar()

    assert {e.id for e in resultado} == {supino.id, esteira.id}


def test_lista_filtrando_por_tipo():
    supino = Exercicio(id=uuid.uuid4(), nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    esteira = Exercicio(id=uuid.uuid4(), nome="Esteira", tipo=TipoExercicio.AEROBICO)
    use_case = ListarExercicios(FakeExercicioRepository([supino, esteira]))

    resultado = use_case.executar(tipo=TipoExercicio.AEROBICO)

    assert [e.id for e in resultado] == [esteira.id]
