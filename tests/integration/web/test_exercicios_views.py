import uuid

from fastapi.testclient import TestClient

from app.infrastructure.auth.jwt import JwtTokenGenerator
from app.main import app

client = TestClient(app, follow_redirects=False)


def _auth_cookies() -> dict[str, str]:
    token = JwtTokenGenerator().generate(uuid.uuid4())
    return {"access_token": token, "csrf_token": "test-csrf-token"}


def _usar_db_session(monkeypatch, db_session):
    from app.infrastructure.web import deps

    monkeypatch.setattr(deps, "get_session_local", lambda: (lambda: db_session))


def test_lista_sem_cookie_redireciona_para_login(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/exercicios")

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_lista_pagina_html(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)

    response = client.get("/exercicios", cookies=_auth_cookies())

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_criar_via_formulario_redireciona_para_lista(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/exercicios/novo",
        data={"nome": nome, "tipo": "musculacao", "csrf_token": "test-csrf-token"},
        cookies=_auth_cookies(),
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/exercicios"


def test_criar_sem_csrf_token_retorna_403(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/exercicios/novo",
        data={"nome": nome, "tipo": "musculacao"},
        cookies=_auth_cookies(),
    )

    assert response.status_code == 403


def test_criar_nome_duplicado_reexibe_formulario_com_erro(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    cookies = _auth_cookies()
    nome = f"Supino Teste {uuid.uuid4().hex[:8]}"

    client.post(
        "/exercicios/novo",
        data={"nome": nome, "tipo": "musculacao", "csrf_token": "test-csrf-token"},
        cookies=cookies,
    )
    duplicado = client.post(
        "/exercicios/novo",
        data={"nome": nome.upper(), "tipo": "musculacao", "csrf_token": "test-csrf-token"},
        cookies=cookies,
    )

    assert duplicado.status_code == 409
    assert "ja cadastrado" in duplicado.text.lower()


def test_remover_via_formulario_redireciona_para_lista(db_session, monkeypatch):
    _usar_db_session(monkeypatch, db_session)
    cookies = _auth_cookies()
    nome = f"Agachamento Teste {uuid.uuid4().hex[:8]}"

    from app.domain.entities.exercicio import Exercicio, TipoExercicio
    from app.infrastructure.db.repositories.exercicio_repository import (
        SqlAlchemyExercicioRepository,
    )

    exercicio = Exercicio(id=uuid.uuid4(), nome=nome, tipo=TipoExercicio.MUSCULACAO)
    SqlAlchemyExercicioRepository(db_session).add(exercicio)
    db_session.commit()

    response = client.post(
        f"/exercicios/{exercicio.id}/remover",
        data={"csrf_token": "test-csrf-token"},
        cookies=cookies,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/exercicios"
