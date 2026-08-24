import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.application.use_cases.criar_exercicio import CriarExercicio
from app.application.use_cases.editar_exercicio import EditarExercicio
from app.application.use_cases.exercicio_errors import (
    ExercicioNaoEncontradoError,
    ExercicioNomeDuplicadoError,
)
from app.application.use_cases.listar_exercicios import ListarExercicios
from app.application.use_cases.remover_exercicio import RemoverExercicio
from app.domain.entities.exercicio import TipoExercicio
from app.infrastructure.db.repositories.exercicio_repository import (
    SqlAlchemyExercicioRepository,
)
from app.infrastructure.web.current_user import get_current_user
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.schemas import ExercicioCreate, ExercicioResponse, ExercicioUpdate

router = APIRouter(prefix="/api/exercicios", tags=["exercicios"])


@router.get("", response_model=list[ExercicioResponse])
def listar(
    tipo: TipoExercicio | None = Query(default=None),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user),
) -> list[ExercicioResponse]:
    exercicios = ListarExercicios(SqlAlchemyExercicioRepository(db)).executar(tipo)
    return [ExercicioResponse(id=e.id, nome=e.nome, tipo=e.tipo) for e in exercicios]


@router.post("", response_model=ExercicioResponse, status_code=201)
def criar(
    payload: ExercicioCreate,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user),
) -> ExercicioResponse:
    use_case = CriarExercicio(SqlAlchemyExercicioRepository(db))
    try:
        exercicio = use_case.executar(payload.nome, payload.tipo)
    except ExercicioNomeDuplicadoError as exc:
        raise HTTPException(status_code=409, detail="Nome ja cadastrado") from exc
    db.commit()
    return ExercicioResponse(id=exercicio.id, nome=exercicio.nome, tipo=exercicio.tipo)


@router.put("/{exercicio_id}", response_model=ExercicioResponse)
def editar(
    exercicio_id: uuid.UUID,
    payload: ExercicioUpdate,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user),
) -> ExercicioResponse:
    use_case = EditarExercicio(SqlAlchemyExercicioRepository(db))
    try:
        exercicio = use_case.executar(exercicio_id, payload.nome, payload.tipo)
    except ExercicioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado") from exc
    except ExercicioNomeDuplicadoError as exc:
        raise HTTPException(status_code=409, detail="Nome ja cadastrado") from exc
    db.commit()
    return ExercicioResponse(id=exercicio.id, nome=exercicio.nome, tipo=exercicio.tipo)


@router.delete("/{exercicio_id}", status_code=204)
def remover(
    exercicio_id: uuid.UUID,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user),
) -> None:
    use_case = RemoverExercicio(SqlAlchemyExercicioRepository(db))
    try:
        use_case.executar(exercicio_id)
    except ExercicioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado") from exc
    db.commit()
