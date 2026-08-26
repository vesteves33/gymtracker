import pytest

from app.infrastructure.auth.secret_check import validate_jwt_secret


def test_aceita_segredo_forte():
    validate_jwt_secret("a" * 32)


@pytest.mark.parametrize("secret", [None, "", "changeme", "curto"])
def test_rejeita_segredo_invalido(secret):
    with pytest.raises(RuntimeError):
        validate_jwt_secret(secret)
