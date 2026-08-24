from app.domain.ports.password_hasher import PasswordHasher
from app.domain.ports.token_generator import TokenGenerator
from app.domain.ports.usuario_repository import UsuarioRepository


class CredenciaisInvalidasError(Exception):
    pass


class AutenticarUsuario:
    def __init__(
        self,
        usuario_repository: UsuarioRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ) -> None:
        self._usuario_repository = usuario_repository
        self._password_hasher = password_hasher
        self._token_generator = token_generator

    def executar(self, login: str, senha: str) -> str:
        usuario = self._usuario_repository.get_by_login(login)
        if usuario is None:
            raise CredenciaisInvalidasError()
        if not self._password_hasher.verify(senha, usuario.senha_hash):
            raise CredenciaisInvalidasError()
        return self._token_generator.generate(usuario.id)
