from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.application.use_cases.autenticar_usuario import (
    AutenticarUsuario,
    CredenciaisInvalidasError,
)
from app.application.use_cases.criar_usuario import (
    CriarUsuario,
    SenhaFracaError,
    UsuarioLoginDuplicadoError,
)
from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.infrastructure.web.deps import get_db
from app.infrastructure.web.rate_limit import LoginRateLimiter
from app.infrastructure.web.schemas import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])
_login_rate_limiter = LoginRateLimiter()


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)
) -> LoginResponse:
    chave = f"{request.client.host if request.client else 'unknown'}:{payload.login}"
    if _login_rate_limiter.esta_bloqueado(chave):
        raise HTTPException(status_code=429, detail="Muitas tentativas, tente novamente mais tarde")

    use_case = AutenticarUsuario(
        usuario_repository=SqlAlchemyUsuarioRepository(db),
        password_hasher=BcryptPasswordHasher(),
        token_generator=JwtTokenGenerator(),
    )
    try:
        token = use_case.executar(payload.login, payload.senha)
    except CredenciaisInvalidasError as exc:
        _login_rate_limiter.registrar_tentativa(chave)
        raise HTTPException(status_code=401, detail="Credenciais invalidas") from exc

    response.set_cookie("access_token", token, httponly=True)
    return LoginResponse(access_token=token)


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"detail": "ok"}


@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> SignupResponse:
    use_case = CriarUsuario(
        usuario_repository=SqlAlchemyUsuarioRepository(db),
        password_hasher=BcryptPasswordHasher(),
    )
    try:
        usuario_id = use_case.executar(payload.login, payload.senha)
    except UsuarioLoginDuplicadoError as exc:
        raise HTTPException(status_code=409, detail="Login ja cadastrado") from exc
    except SenhaFracaError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    db.commit()
    return SignupResponse(id=usuario_id, login=payload.login)
