import uuid

import pytest

from app.application.use_cases.criar_usuario import (
    CriarUsuario,
    SenhaFracaError,
    UsuarioLoginDuplicadoError,
)
from app.domain.entities.usuario import Usuario


class FakeUsuarioRepository:
    def __init__(self, usuarios: list[Usuario] | None = None) -> None:
        self._usuarios = usuarios or []

    def get_by_login(self, login: str) -> Usuario | None:
        return next((u for u in self._usuarios if u.login == login), None)

    def add(self, usuario: Usuario) -> None:
        self._usuarios.append(usuario)


class FakePasswordHasher:
    def hash(self, senha: str) -> str:
        return f"hash:{senha}"

    def verify(self, senha: str, senha_hash: str) -> bool:
        return senha_hash == f"hash:{senha}"


def test_cria_usuario_com_senha_forte():
    repo = FakeUsuarioRepository()
    use_case = CriarUsuario(repo, FakePasswordHasher())

    usuario_id = use_case.executar("vitor", "Senha123forte")

    assert isinstance(usuario_id, uuid.UUID)
    assert repo.get_by_login("vitor") is not None


def test_rejeita_login_duplicado():
    repo = FakeUsuarioRepository([Usuario(id=uuid.uuid4(), login="vitor", senha_hash="x")])
    use_case = CriarUsuario(repo, FakePasswordHasher())

    with pytest.raises(UsuarioLoginDuplicadoError):
        use_case.executar("vitor", "Senha123forte")


@pytest.mark.parametrize(
    "senha",
    ["curta1", "somenteletras", "12345678", ""],
)
def test_rejeita_senha_fraca(senha):
    repo = FakeUsuarioRepository()
    use_case = CriarUsuario(repo, FakePasswordHasher())

    with pytest.raises(SenhaFracaError):
        use_case.executar("vitor", senha)
