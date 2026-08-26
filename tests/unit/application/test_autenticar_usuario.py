import uuid

import pytest

from app.application.use_cases.autenticar_usuario import (
    AutenticarUsuario,
    CredenciaisInvalidasError,
)
from app.domain.entities.usuario import Usuario
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.token_generator import TokenGenerator
from app.domain.ports.usuario_repository import UsuarioRepository


class FakeUsuarioRepository(UsuarioRepository):
    def __init__(self, usuarios: list[Usuario]) -> None:
        self._usuarios = {u.login: u for u in usuarios}

    def get_by_login(self, login: str) -> Usuario | None:
        return self._usuarios.get(login)

    def add(self, usuario: Usuario) -> None:
        self._usuarios[usuario.login] = usuario

    def existe_algum_usuario(self) -> bool:
        return len(self._usuarios) > 0


class FakePasswordHasher(PasswordHasher):
    def hash(self, senha: str) -> str:
        return f"hash:{senha}"

    def verify(self, senha: str, senha_hash: str) -> bool:
        return senha_hash == f"hash:{senha}"


class FakeTokenGenerator(TokenGenerator):
    def generate(self, usuario_id: uuid.UUID) -> str:
        return f"token:{usuario_id}"


def test_autentica_usuario_com_credenciais_validas():
    usuario = Usuario(id=uuid.uuid4(), login="vitor", senha_hash="hash:123456")
    use_case = AutenticarUsuario(
        usuario_repository=FakeUsuarioRepository([usuario]),
        password_hasher=FakePasswordHasher(),
        token_generator=FakeTokenGenerator(),
    )

    token = use_case.executar("vitor", "123456")

    assert token == f"token:{usuario.id}"


def test_recusa_login_inexistente():
    use_case = AutenticarUsuario(
        usuario_repository=FakeUsuarioRepository([]),
        password_hasher=FakePasswordHasher(),
        token_generator=FakeTokenGenerator(),
    )

    with pytest.raises(CredenciaisInvalidasError):
        use_case.executar("desconhecido", "123456")


def test_recusa_senha_incorreta():
    usuario = Usuario(id=uuid.uuid4(), login="vitor", senha_hash="hash:123456")
    use_case = AutenticarUsuario(
        usuario_repository=FakeUsuarioRepository([usuario]),
        password_hasher=FakePasswordHasher(),
        token_generator=FakeTokenGenerator(),
    )

    with pytest.raises(CredenciaisInvalidasError):
        use_case.executar("vitor", "senha-errada")
