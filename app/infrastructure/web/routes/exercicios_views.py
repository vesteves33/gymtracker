import uuid
from dataclasses import dataclass

from fastapi import APIRouter, Cookie, Depends, Form, HTTPException, Request, Response
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
from app.infrastructure.web.csrf import (
    CSRF_COOKIE_NAME,
    copy_set_cookie_headers,
    ensure_csrf_cookie,
    verify_csrf_token,
)
from app.infrastructure.web.current_user import get_current_user_view
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.templates import templates


@dataclass
class ExercicioFormState:
    nome: str
    tipo: TipoExercicio
    id: uuid.UUID | None = None


router = APIRouter(prefix="/exercicios")


@router.get("")
def listar_pagina(
    request: Request,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    exercicios = ListarExercicios(SqlAlchemyExercicioRepository(db)).executar()
    draft = Response()
    csrf_token = ensure_csrf_cookie(draft, csrf_token_cookie)
    response = templates.TemplateResponse(
        request, "exercicios/list.html", {"exercicios": exercicios, "csrf_token": csrf_token}
    )
    copy_set_cookie_headers(draft, response)
    return response


@router.get("/novo")
def form_novo(
    request: Request,
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    draft = Response()
    csrf_token = ensure_csrf_cookie(draft, csrf_token_cookie)
    response = templates.TemplateResponse(
        request,
        "exercicios/form.html",
        {"exercicio": None, "erro": None, "csrf_token": csrf_token},
    )
    copy_set_cookie_headers(draft, response)
    return response


@router.post("/novo")
def criar_pagina(
    request: Request,
    nome: str = Form(..., max_length=100),
    tipo: TipoExercicio = Form(...),
    csrf_token: str | None = Form(default=None),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    verify_csrf_token(csrf_token_cookie, csrf_token)
    use_case = CriarExercicio(SqlAlchemyExercicioRepository(db))
    try:
        use_case.executar(nome, tipo)
    except ExercicioNomeDuplicadoError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {
                "exercicio": ExercicioFormState(nome=nome, tipo=tipo),
                "erro": "Nome ja cadastrado",
                "csrf_token": csrf_token,
            },
            status_code=409,
        )
    except ValueError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {
                "exercicio": ExercicioFormState(nome=nome, tipo=tipo),
                "erro": "Nome nao pode ser vazio",
                "csrf_token": csrf_token,
            },
            status_code=422,
        )
    db.commit()
    return RedirectResponse(url="/exercicios", status_code=303)


@router.get("/{exercicio_id}/editar")
def form_editar(
    request: Request,
    exercicio_id: uuid.UUID,
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    exercicio = SqlAlchemyExercicioRepository(db).get_by_id(exercicio_id)
    if exercicio is None:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado")
    draft = Response()
    csrf_token = ensure_csrf_cookie(draft, csrf_token_cookie)
    response = templates.TemplateResponse(
        request,
        "exercicios/form.html",
        {"exercicio": exercicio, "erro": None, "csrf_token": csrf_token},
    )
    copy_set_cookie_headers(draft, response)
    return response


@router.post("/{exercicio_id}/editar")
def editar_pagina(
    request: Request,
    exercicio_id: uuid.UUID,
    nome: str = Form(..., max_length=100),
    tipo: TipoExercicio = Form(...),
    csrf_token: str | None = Form(default=None),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    verify_csrf_token(csrf_token_cookie, csrf_token)
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
                "exercicio": ExercicioFormState(id=exercicio_id, nome=nome, tipo=tipo),
                "erro": "Nome ja cadastrado",
                "csrf_token": csrf_token,
            },
            status_code=409,
        )
    except ValueError:
        return templates.TemplateResponse(
            request,
            "exercicios/form.html",
            {
                "exercicio": ExercicioFormState(id=exercicio_id, nome=nome, tipo=tipo),
                "erro": "Nome nao pode ser vazio",
                "csrf_token": csrf_token,
            },
            status_code=422,
        )
    db.commit()
    return RedirectResponse(url="/exercicios", status_code=303)


@router.post("/{exercicio_id}/remover")
def remover_pagina(
    exercicio_id: uuid.UUID,
    csrf_token: str | None = Form(default=None),
    db: Session = Depends(get_db),
    _usuario_id: uuid.UUID = Depends(get_current_user_view),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    verify_csrf_token(csrf_token_cookie, csrf_token)
    try:
        RemoverExercicio(SqlAlchemyExercicioRepository(db)).executar(exercicio_id)
    except ExercicioNaoEncontradoError as exc:
        raise HTTPException(status_code=404, detail="Exercicio nao encontrado") from exc
    db.commit()
    return RedirectResponse(url="/exercicios", status_code=303)
