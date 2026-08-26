import uuid

import jwt
from fastapi import Cookie, Header, HTTPException

from app.infrastructure.auth.jwt import JwtTokenGenerator


class UsuarioNaoAutenticadoView(Exception):
    pass


def get_current_user_view(
    access_token: str | None = Cookie(default=None),
) -> uuid.UUID:
    if access_token is None:
        raise UsuarioNaoAutenticadoView()
    try:
        return JwtTokenGenerator.decode(access_token)
    except (jwt.PyJWTError, ValueError, KeyError) as exc:
        raise UsuarioNaoAutenticadoView() from exc


def get_current_user(
    access_token: str | None = Cookie(default=None),
    authorization: str | None = Header(default=None),
) -> uuid.UUID:
    token = access_token
    if token is None and authorization is not None and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ")
    if token is None:
        raise HTTPException(status_code=401, detail="Nao autenticado")

    try:
        return JwtTokenGenerator.decode(token)
    except (jwt.PyJWTError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=401, detail="Token invalido") from exc
