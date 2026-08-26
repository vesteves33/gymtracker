import logging
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
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
from app.infrastructure.web.current_user import get_current_user_view
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.templates import templates

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exercicios")


@router.get("")
def listar_pagina(
    request: Request,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    exercicios = ListarExercicios(SqlAlchemyExercicioRepository(db)).executar()
    return templates.TemplateResponse(request, "exercicios/list.html", {"exercicios": exercicios})


@router.get("/novo")
def form_novo(
    request: Request,
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    return templates.TemplateResponse(
        request, "exercicios/form.html", {"exercicio": None, "erro": None}
    )


@router.post("/novo")
def criar_pagina(
    request: Request,
    nome: str = Form(..., max_length=100),
    tipo: TipoExercicio = Form(...),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    use_case = CriarExercicio(SqlAlchemyExercicioRepository(db))
    try:
        use_case.executar(nome, tipo)
    except ExercicioNomeDuplicadoError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {"exercicio": {"nome": nome, "tipo": tipo}, "erro": "Nome ja cadastrado"},
            status_code=409,
        )
    except ValueError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {"exercicio": {"nome": nome, "tipo": tipo}, "erro": "Nome nao pode ser vazio"},
            status_code=422,
        )
    db.commit()
    logger.info("exercicio_criado nome=%s tipo=%s", nome, tipo)
    return RedirectResponse(url="/exercicios", status_code=303)


@router.get("/{exercicio_id}/editar")
def form_editar(
    request: Request,
    exercicio_id: uuid.UUID,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    exercicio = SqlAlchemyExercicioRepository(db).get_by_id(exercicio_id)
    if exercicio is None:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado")
    return templates.TemplateResponse(
        request, "exercicios/form.html", {"exercicio": exercicio, "erro": None}
    )


@router.post("/{exercicio_id}/editar")
def editar_pagina(
    request: Request,
    exercicio_id: uuid.UUID,
    nome: str = Form(..., max_length=100),
    tipo: TipoExercicio = Form(...),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    use_case = EditarExercicio(SqlAlchemyExercicioRepository(db))
    try:
        use_case.executar(exercicio_id, nome, tipo)
    except ExercicioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado") from exc
    except ExercicioNomeDuplicadoError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {
                "exercicio": {"id": exercicio_id, "nome": nome, "tipo": tipo},
                "erro": "Nome ja cadastrado",
            },
            status_code=409,
        )
    except ValueError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {
                "exercicio": {"id": exercicio_id, "nome": nome, "tipo": tipo},
                "erro": "Nome nao pode ser vazio",
            },
            status_code=422,
        )
    db.commit()
    logger.info("exercicio_editado id=%s nome=%s", exercicio_id, nome)
    return RedirectResponse(url="/exercicios", status_code=303)


@router.post("/{exercicio_id}/remover")
def remover_pagina(
    exercicio_id: uuid.UUID,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
):
    try:
        RemoverExercicio(SqlAlchemyExercicioRepository(db)).executar(exercicio_id)
    except ExercicioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado") from exc
    db.commit()
    logger.info("exercicio_removido id=%s", exercicio_id)
    return RedirectResponse(url="/exercicios", status_code=303)
