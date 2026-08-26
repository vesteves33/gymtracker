import uuid

import pytest

from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.web.current_user import (
    UsuarioNaoAutenticadoView,
    get_current_user_view,
)


def test_sem_cookie_levanta_nao_autenticado():
    with pytest.raises(UsuarioNaoAutenticadoView):
        get_current_user_view(access_token=None)


def test_cookie_invalido_levanta_nao_autenticado():
    with pytest.raises(UsuarioNaoAutenticadoView):
        get_current_user_view(access_token="token-invalido")


def test_cookie_valido_retorna_usuario_id(monkeypatch):
    usuario_id = uuid.uuid4()
    monkeypatch.setenv("JWT_SECRET", "segredo-teste")
    token = JwtTokenGenerator().generate(usuario_id)

    resultado = get_current_user_view(access_token=token)

    assert resultado == usuario_id
