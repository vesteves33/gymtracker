import uuid
from dataclasses import dataclass
from enum import Enum


class TipoExercicio(str, Enum):
    MUSCULACAO = "musculacao"
    AEROBICO = "aerobico"


@dataclass
class Exercicio:
    id: uuid.UUID
    nome: str
    tipo: TipoExercicio
