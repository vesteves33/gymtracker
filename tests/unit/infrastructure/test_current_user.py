import uuid
from datetime import datetime, timedelta, timezone

import jwt as pyjwt
import pytest
from fastapi import HTTPException

from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.web.current_user import get_current_user


def test_retorna_usuario_id_com_cookie_valido(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    usuario_id = uuid.uuid4()
    token = JwtTokenGenerator().generate(usuario_id)

    resultado = get_current_user(access_token=token, authorization=None)

    assert resultado == usuario_id


def test_retorna_usuario_id_com_header_bearer(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    usuario_id = uuid.uuid4()
    token = JwtTokenGenerator().generate(usuario_id)

    resultado = get_current_user(access_token=None, authorization=f"Bearer {token}")

    assert resultado == usuario_id


def test_sem_token_levanta_401():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(access_token=None, authorization=None)

    assert exc_info.value.status_code == 401


def test_token_invalido_levanta_401(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(access_token="token-invalido", authorization=None)

    assert exc_info.value.status_code == 401


def test_token_sem_sub_levanta_401(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    payload = {"exp": datetime.now(timezone.utc) + timedelta(minutes=5)}
    token = pyjwt.encode(payload, "test-secret", algorithm="HS256")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(access_token=token, authorization=None)

    assert exc_info.value.status_code == 401
