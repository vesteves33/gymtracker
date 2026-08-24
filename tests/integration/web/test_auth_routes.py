import uuid

from fastapi.testclient import TestClient

from app.domain.entities.usuario import Usuario
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.main import app

client = TestClient(app)


def test_login_com_credenciais_validas_retorna_token(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "SessionLocal", lambda: db_session)

    hasher = BcryptPasswordHasher()
    usuario = Usuario(id=uuid.uuid4(), login="vitor", senha_hash=hasher.hash("123456"))
    SqlAlchemyUsuarioRepository(db_session).add(usuario)
    db_session.commit()

    response = client.post("/api/auth/login", json={"login": "vitor", "senha": "123456"})

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "access_token" in response.cookies


def test_login_com_credenciais_invalidas_retorna_401(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "SessionLocal", lambda: db_session)

    response = client.post("/api/auth/login", json={"login": "inexistente", "senha": "x"})

    assert response.status_code == 401
