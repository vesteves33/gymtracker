import uuid

from app.application.use_cases.exercicio_errors import ExercicioNomeDuplicadoError
from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository


class CriarExercicio:
    def __init__(self, exercicio_repository: ExercicioRepository) -> None:
        self._exercicio_repository = exercicio_repository

    def executar(self, nome: str, tipo: TipoExercicio) -> Exercicio:
        nome = nome.strip()
        if not nome:
            raise ValueError("nome nao pode ser vazio")
        if self._exercicio_repository.get_by_nome(nome) is not None:
            raise ExercicioNomeDuplicadoError()

        exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=tipo)
        self._exercicio_repository.add(exercicio)
        return exercicio
