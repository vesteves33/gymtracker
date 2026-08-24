import uuid
from abc import ABC, abstractmethod


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self, usuario_id: uuid.UUID) -> str: ...
