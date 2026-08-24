import uuid

from pydantic import BaseModel, Field

from app.domain.entities.exercicio import TipoExercicio


class LoginRequest(BaseModel):
    login: str
    senha: str = Field(max_length=72)


class LoginResponse(BaseModel):
    access_token: str


class ExercicioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    tipo: TipoExercicio


class ExercicioUpdate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    tipo: TipoExercicio


class ExercicioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    tipo: TipoExercicio
