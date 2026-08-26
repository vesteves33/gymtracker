import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.exercicio import Exercicio, TipoExercicio
from app.domain.ports.exercicio_repository import ExercicioRepository
from app.infrastructure.db.models import ExercicioModel


class SqlAlchemyExercicioRepository(ExercicioRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, exercicio_id: uuid.UUID) -> Exercicio | None:
        model = self._session.get(ExercicioModel, exercicio_id)
        if model is None:
            return None
        return self._to_entity(model)

    def get_by_nome(self, nome: str) -> Exercicio | None:
        model = (
            self._session.query(ExercicioModel)
            .filter(func.lower(ExercicioModel.nome) == nome.lower())
            .first()
        )
        if model is None:
            return None
        return self._to_entity(model)

    def list_all(self, tipo: TipoExercicio | None = None) -> list[Exercicio]:
        query = self._session.query(ExercicioModel)
        if tipo is not None:
            query = query.filter_by(tipo=tipo.value)
        return [self._to_entity(model) for model in query.order_by(ExercicioModel.nome)]

    def add(self, exercicio: Exercicio) -> None:
        model = ExercicioModel(id=exercicio.id, nome=exercicio.nome, tipo=exercicio.tipo.value)
        self._session.add(model)
        self._session.flush()

    def update(self, exercicio: Exercicio) -> None:
        model = self._session.get(ExercicioModel, exercicio.id)
        model.nome = exercicio.nome
        model.tipo = exercicio.tipo.value
        self._session.flush()

    def delete(self, exercicio_id: uuid.UUID) -> None:
        model = self._session.get(ExercicioModel, exercicio_id)
        self._session.delete(model)
        self._session.flush()

    @staticmethod
    def _to_entity(model: ExercicioModel) -> Exercicio:
        return Exercicio(id=model.id, nome=model.nome, tipo=TipoExercicio(model.tipo))
