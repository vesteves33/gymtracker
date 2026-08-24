from abc import ABC, abstractmethod
import uuid


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self, usuario_id: uuid.UUID) -> str: ...
