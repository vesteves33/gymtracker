from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.ports.usuario_repository import UsuarioRepository
from app.infrastructure.db.models import UsuarioModel


class SqlAlchemyUsuarioRepository(UsuarioRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_login(self, login: str) -> Usuario | None:
        model = self._session.query(UsuarioModel).filter_by(login=login).first()
        if model is None:
            return None
        return Usuario(id=model.id, login=model.login, senha_hash=model.senha_hash)

    def add(self, usuario: Usuario) -> None:
        model = UsuarioModel(
            id=usuario.id, login=usuario.login, senha_hash=usuario.senha_hash
        )
        self._session.add(model)
        self._session.flush()

    def existe_algum_usuario(self) -> bool:
        return self._session.query(UsuarioModel).first() is not None
