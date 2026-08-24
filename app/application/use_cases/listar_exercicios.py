from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class ListarExercicios:
    def __init__(self, exercicio_repository: ExercicioRepository) -> None:
        self._exercicio_repository = exercicio_repository

    def executar(self, tipo: TipoExercicio | None = None) -> list[Exercicio]:
        return self._exercicio_repository.list_all(tipo)
