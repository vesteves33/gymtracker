import importlib
import os

import pytest


def test_importar_session_sem_database_url_nao_quebra(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    import app.infrastructure.db.session as session_module

    importlib.reload(session_module)

    assert hasattr(session_module, "get_engine")
    assert hasattr(session_module, "get_session_local")


def test_get_engine_levanta_erro_claro_sem_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    import app.infrastructure.db.session as session_module

    importlib.reload(session_module)

    with pytest.raises(KeyError):
        session_module.get_engine()

    # restaura estado para nao afetar outros testes do processo
    monkeypatch.setenv(
        "DATABASE_URL",
        os.environ.get(
            "DATABASE_URL",
            "postgresql+psycopg2://gymtracker:gymtracker@localhost:5432/gymtracker",
        ),
    )
    importlib.reload(session_module)
