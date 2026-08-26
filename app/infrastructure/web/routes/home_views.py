from fastapi import APIRouter, Cookie, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.application.use_cases.autenticar_usuario import (
    AutenticarUsuario,
    CredenciaisInvalidasError,
)
from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.infrastructure.web.csrf import (
    CSRF_COOKIE_NAME,
    copy_set_cookie_headers,
    ensure_csrf_cookie,
    verify_csrf_token,
)
from app.infrastructure.web.current_user import UsuarioNaoAutenticadoView, get_current_user_view
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.templates import templates

router = APIRouter()


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    try:
        get_current_user_view(access_token=request.cookies.get("access_token"))
    except UsuarioNaoAutenticadoView:
        draft = Response()
        csrf_token = ensure_csrf_cookie(draft, csrf_token_cookie)
        response = templates.TemplateResponse(
            request, "login.html", {"erro": None, "csrf_token": csrf_token}
        )
        copy_set_cookie_headers(draft, response)
        return response
    return RedirectResponse(url="/exercicios", status_code=303)


@router.post("/")
def autenticar(
    request: Request,
    login: str = Form(...),
    senha: str = Form(...),
    csrf_token: str | None = Form(default=None),
    db: Session = Depends(get_db),
    csrf_token_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE_NAME),
):
    verify_csrf_token(csrf_token_cookie, csrf_token)
    use_case = AutenticarUsuario(
        usuario_repository=SqlAlchemyUsuarioRepository(db),
        password_hasher=BcryptPasswordHasher(),
        token_generator=JwtTokenGenerator(),
    )
    try:
        token = use_case.executar(login, senha)
    except CredenciaisInvalidasError:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"erro": "Credenciais invalidas", "csrf_token": csrf_token},
            status_code=401,
        )
    redirect = RedirectResponse(url="/exercicios", status_code=303)
    redirect.set_cookie("access_token", token, httponly=True)
    return redirect


@router.post("/logout")
def logout():
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie("access_token")
    return redirect
