import uuid

from fastapi.testclient import TestClient

from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.main import app

client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    token = JwtTokenGenerator().generate(uuid.uuid4())
    return {"Authorization": f"Bearer {token}"}


def _usar_db_session(monkeypatch, db_session):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))


def test_listar_sem_token_retorna_401(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/api/exercicios")

    assert response.status_code == 401


def test_criar_listar_editar_remover_exercicio(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    headers = _auth_headers()
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    criar = client.post(
        "/api/exercicios", json={"nome": nome, "tipo": "musculacao"}, headers=headers
    )
    assert criar.status_code == 201
    exercicio_id = criar.json()["id"]

    listar = client.get("/api/exercicios", headers=headers)
    assert listar.status_code == 200
    assert any(e["id"] == exercicio_id for e in listar.json())

    editar = client.put(
        f"/api/exercicios/{exercicio_id}",
        json={"nome": f"{nome} reto", "tipo": "musculacao"},
        headers=headers,
    )
    assert editar.status_code == 200
    assert editar.json()["nome"] == f"{nome} reto"

    remover = client.delete(f"/api/exercicios/{exercicio_id}", headers=headers)
    assert remover.status_code == 204

    listar_apos = client.get("/api/exercicios", headers=headers)
    assert not any(e["id"] == exercicio_id for e in listar_apos.json())


def test_criar_nome_duplicado_retorna_409(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    headers = _auth_headers()
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    client.post("/api/exercicios", json={"nome": nome, "tipo": "musculacao"}, headers=headers)
    duplicado = client.post(
        "/api/exercicios", json={"nome": nome.lower(), "tipo": "musculacao"}, headers=headers
    )

    assert duplicado.status_code == 409


def test_editar_id_inexistente_retorna_404(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    headers = _auth_headers()
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    response = client.put(
        f"/api/exercicios/{uuid.uuid4()}",
        json={"nome": nome, "tipo": "musculacao"},
        headers=headers,
    )

    assert response.status_code == 404


def test_criar_tipo_invalido_retorna_422(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    headers = _auth_headers()
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/api/exercicios", json={"nome": nome, "tipo": "invalido"}, headers=headers
    )

    assert response.status_code == 422


def test_criar_nome_vazio_retorna_422(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    headers = _auth_headers()

    response = client.post(
        "/api/exercicios", json={"nome": "   ", "tipo": "musculacao"}, headers=headers
    )

    assert response.status_code == 422
