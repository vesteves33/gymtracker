import re
import uuid

from app.domain.entities.usuario import Usuario
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.usuario_repository import UsuarioRepository

SENHA_MIN_LENGTH = 8
SENHA_REGEX_LETRA = re.compile(r"[A-Za-z]")
SENHA_REGEX_DIGITO = re.compile(r"\d")


class UsuarioLoginDuplicadoError(Exception):
    pass


class SenhaFracaError(Exception):
    pass


def _validar_senha(senha: str) -> None:
    if (
        len(senha) < SENHA_MIN_LENGTH
        or not SENHA_REGEX_LETRA.search(senha)
        or not SENHA_REGEX_DIGITO.search(senha)
    ):
        raise SenhaFracaError(
            f"Senha deve ter pelo menos {SENHA_MIN_LENGTH} caracteres, com letras e numeros"
        )


class CriarUsuario:
    def __init__(
        self, usuario_repository: UsuarioRepository, password_hasher: PasswordHasher
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher

    def executar(self, login: str, senha: str) -> uuid.UUID:
        _validar_senha(senha)
        if self._usuario_repository.get_by_login(login) is not None:
            raise UsuarioLoginDuplicadoError()

        usuario_id = uuid.uuid4()
        usuario = Usuario(id=usuario_id, login=login, senha_hash=self._password_hasher.hash(senha))
        self._usuario_repository.add(usuario)
        return usuario_id
