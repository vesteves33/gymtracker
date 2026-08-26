import uuid

from fastapi.testclient import TestClient

from app.domain.entities.usuario import Usuario
from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.main import app

client = TestClient(app, follow_redirects=False)


def _usar_db_session(monkeypatch, db_session):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "SessionLocal", lambda: db_session)


def _auth_cookies() -> dict[str, str]:
    token = JwtTokenGenerator().generate(uuid.uuid4())
    return {"access_token": token}


def test_home_sem_cookie_mostra_form_login(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<form" in response.text.lower()


def test_home_com_cookie_valido_redireciona_para_exercicios(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/", cookies=_auth_cookies())

    assert response.status_code == 303
    assert response.headers["location"] == "/exercicios"


def test_home_com_cookie_invalido_mostra_form_login(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/", cookies={"access_token": "invalido"})

    assert response.status_code == 200
    assert "<form" in response.text.lower()


def test_post_login_credenciais_validas_redireciona_e_seta_cookie(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    hasher = BcryptPasswordHasher()
    usuario = Usuario(id=uuid.uuid4(), login="vitor", senha_hash=hasher.hash("123456"))
    SqlAlchemyUsuarioRepository(db_session).add(usuario)
    db_session.commit()

    response = client.post("/", data={"login": "vitor", "senha": "123456"})

    assert response.status_code == 303
    assert response.headers["location"] == "/exercicios"
    assert "access_token" in response.cookies


def test_post_login_credenciais_invalidas_reexibe_form_com_erro(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.post("/", data={"login": "inexistente", "senha": "x"})

    assert response.status_code == 401
    assert "credenciais" in response.text.lower()


def test_logout_remove_cookie_e_redireciona(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.post("/logout", cookies=_auth_cookies())

    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert response.cookies.get("access_token") is None
