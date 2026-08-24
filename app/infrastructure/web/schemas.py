from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    login: str
    senha: str = Field(max_length=72)


class LoginResponse(BaseModel):
    access_token: str
