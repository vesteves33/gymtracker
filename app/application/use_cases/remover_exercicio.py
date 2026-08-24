import uuid

from app.application.use_cases.exercicio_errors import ExercicioNaoEncontradoError
from app.domain.ports.exercicio_repository import ExercicioRepository


class RemoverExercicio:
    def __init__(self, exercicio_repository: ExercicioRepository) -> None:
        self._exercicio_repository = exercicio_repository

    def executar(self, exercicio_id: uuid.UUID) -> None:
        existente = self._exercicio_repository.get_by_id(exercicio_id)
        if existente is None:
            raise ExercicioNaoEncontradoError()
        self._exercicio_repository.delete(exercicio_id)
