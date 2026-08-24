import uuid
from dataclasses import dataclass


@dataclass
class Usuario:
    id: uuid.UUID
    login: str
    senha_hash: str
