from abc import ABC, abstractmethod

from app.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    @abstractmethod
    def get_by_login(self, login: str) -> Usuario | None: ...

    @abstractmethod
    def add(self, usuario: Usuario) -> None: ...

    @abstractmethod
    def existe_algum_usuario(self) -> bool: ...
