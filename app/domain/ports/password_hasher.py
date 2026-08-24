from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, senha: str) -> str: ...

    @abstractmethod
    def verify(self, senha: str, senha_hash: str) -> bool: ...
