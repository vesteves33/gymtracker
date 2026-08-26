import uuid

from app.application.use_cases.exercicio_errors import (
    ExercicioNaoEncontradoError,
    ExercicioNomeDuplicadoError,
)
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class EditarExercicio:
    def __init__(self, exercicio_repository: ExercicioRepository) -> None:
        self._exercicio_repository = exercicio_repository

    def executar(self, exercicio_id: uuid.UUID, nome: str, tipo: TipoExercicio) -> Exercicio:
        existente = self._exercicio_repository.get_by_id(exercicio_id)
        if existente is None:
            raise ExercicioNaoEncontradoError()

        nome = nome.strip()
        if not nome:
            raise ValueError("nome nao pode ser vazio")

        duplicado = self._exercicio_repository.get_by_nome(nome)
        if duplicado is not None and duplicado.id != exercicio_id:
            raise ExercicioNomeDuplicadoError()

        atualizado = Exercicio(id=exercicio_id, nome=nome, tipo=tipo)
        self._exercicio_repository.update(atualizado)
        return atualizado
