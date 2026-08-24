import uuid
from abc import ABC, abstractmethod

from app.domain.entities.exercicio import Exercicio, TipoExercicio


class ExercicioRepository(ABC):
    @abstractmethod
    def get_by_id(self, exercicio_id: uuid.UUID) -> Exercicio | None: ...

    @abstractmethod
    def get_by_nome(self, nome: str) -> Exercicio | None: ...

    @abstractmethod
    def list_all(self, tipo: TipoExercicio | None = None) -> list[Exercicio]: ...

    @abstractmethod
    def add(self, exercicio: Exercicio) -> None: ...

    @abstractmethod
    def update(self, exercicio: Exercicio) -> None: ...

    @abstractmethod
    def delete(self, exercicio_id: uuid.UUID) -> None: ...
