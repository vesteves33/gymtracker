from dataclasses import dataclass
import uuid


@dataclass
class Usuario:
    id: uuid.UUID
    login: str
    senha_hash: str
