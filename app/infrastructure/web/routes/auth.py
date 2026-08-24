from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.application.use_cases.autenticar_usuario import (
    AutenticarUsuario,
    CredenciaisInvalidasError,
)
from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest, response: Response, db: Session = Depends(get_db)
) -> LoginResponse:
    use_case = AutenticarUsuario(
        usuario_repository=SqlAlchemyUsuarioRepository(db),
        password_hasher=BcryptPasswordHasher(),
        token_generator=JwtTokenGenerator(),
    )
    try:
        token = use_case.executar(payload.login, payload.senha)
    except CredenciaisInvalidasError as exc:
        raise HTTPException(status_code=401, detail="Credenciais invalidas") from exc

    response.set_cookie("access_token", token, httponly=True)
    return LoginResponse(access_token=token)


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"detail": "ok"}
