import uuid

from fastapi.testclient import TestClient

from app.domain.entities.usuario import Usuario
from app.infrastructure.auth.password import BcryptPasswordHasher
from app.infrastructure.db.repositories.usuario_repository import SqlAlchemyUsuarioRepository
from app.main import app

client = TestClient(app)


def test_login_com_credenciais_validas_retorna_token(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))

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

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))

    response = client.post("/api/auth/login", json={"login": "inexistente", "senha": "x"})

    assert response.status_code == 401


def test_login_com_senha_maior_que_72_caracteres_retorna_422(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))

    response = client.post("/api/auth/login", json={"login": "vitor", "senha": "x" * 100})

    assert response.status_code == 422


def test_login_bloqueado_apos_muitas_tentativas(db_session, monkeypatch):
    from app.infrastructure.web import deps
    from app.infrastructure.web import rate_limit as rate_limit_module

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    monkeypatch.setattr(
        rate_limit_module,
        "login_rate_limiter",
        rate_limit_module.LoginRateLimiter(max_tentativas=2),
    )

    for _ in range(2):
        client.post("/api/auth/login", json={"login": "inexistente", "senha": "x"})

    response = client.post("/api/auth/login", json={"login": "inexistente", "senha": "x"})

    assert response.status_code == 429


def test_signup_com_senha_forte_cria_usuario_e_permite_login(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    login_unico = f"usuario_{uuid.uuid4().hex[:8]}"

    signup_response = client.post(
        "/api/auth/signup", json={"login": login_unico, "senha": "Senha123forte"}
    )
    assert signup_response.status_code == 201

    login_response = client.post(
        "/api/auth/login", json={"login": login_unico, "senha": "Senha123forte"}
    )
    assert login_response.status_code == 200


def test_signup_com_login_duplicado_apos_bootstrap_retorna_403(db_session, monkeypatch):
    # Com o cadastro publico restrito a bootstrap (apenas quando nao ha nenhum usuario),
    # uma segunda tentativa de signup - mesmo com login duplicado - e barrada pelo 403
    # de "cadastro publico desabilitado" antes de chegar na checagem de login duplicado.
    # A checagem de login duplicado em si continua coberta em
    # tests/unit/application/test_criar_usuario.py::test_rejeita_login_duplicado.
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    login_unico = f"usuario_{uuid.uuid4().hex[:8]}"

    client.post("/api/auth/signup", json={"login": login_unico, "senha": "Senha123forte"})
    duplicado = client.post(
        "/api/auth/signup", json={"login": login_unico, "senha": "OutraSenha456"}
    )

    assert duplicado.status_code == 403


def test_signup_com_senha_fraca_retorna_422(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    login_unico = f"usuario_{uuid.uuid4().hex[:8]}"

    response = client.post("/api/auth/signup", json={"login": login_unico, "senha": "curta1"})

    assert response.status_code == 422


def test_signup_com_login_maior_que_50_caracteres_retorna_422(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    login_longo = "a" * 51

    response = client.post(
        "/api/auth/signup", json={"login": login_longo, "senha": "Senha123forte"}
    )

    assert response.status_code == 422


def test_signup_apos_primeiro_usuario_retorna_403(db_session, monkeypatch):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))
    primeiro_login = f"usuario_{uuid.uuid4().hex[:8]}"
    segundo_login = f"usuario_{uuid.uuid4().hex[:8]}"

    primeira_resposta = client.post(
        "/api/auth/signup", json={"login": primeiro_login, "senha": "Senha123forte"}
    )
    assert primeira_resposta.status_code == 201

    segunda_resposta = client.post(
        "/api/auth/signup", json={"login": segundo_login, "senha": "Senha123forte"}
    )

    assert segunda_resposta.status_code == 403
