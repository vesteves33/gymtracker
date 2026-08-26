from pathlib import Path

import pytest

from app.infrastructure.db.migrations.paths import find_project_root


def test_encontra_raiz_a_partir_de_arquivo_profundo():
    resultado = find_project_root(Path(__file__).resolve())
    assert (resultado / "pyproject.toml").exists()


def test_levanta_erro_se_nao_encontrar(tmp_path):
    with pytest.raises(RuntimeError):
        find_project_root(tmp_path / "sub" / "dir")
