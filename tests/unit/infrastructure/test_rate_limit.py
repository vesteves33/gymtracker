import time

from app.infrastructure.web.rate_limit import LoginRateLimiter


def test_libera_ate_max_tentativas():
    limiter = LoginRateLimiter(max_tentativas=3, janela_segundos=60)
    for _ in range(3):
        assert limiter.esta_bloqueado("vitor") is False
        limiter.registrar_tentativa("vitor")
    assert limiter.esta_bloqueado("vitor") is True


def test_chaves_diferentes_nao_se_afetam():
    limiter = LoginRateLimiter(max_tentativas=1, janela_segundos=60)
    limiter.registrar_tentativa("vitor")
    assert limiter.esta_bloqueado("vitor") is True
    assert limiter.esta_bloqueado("outro") is False


def test_janela_expira_e_libera(monkeypatch):
    limiter = LoginRateLimiter(max_tentativas=1, janela_segundos=1)
    limiter.registrar_tentativa("vitor")
    assert limiter.esta_bloqueado("vitor") is True
    time.sleep(1.1)
    assert limiter.esta_bloqueado("vitor") is False


def test_esta_bloqueado_nao_cria_entradas_para_chaves_nunca_registradas():
    limiter = LoginRateLimiter(max_tentativas=3, janela_segundos=60)

    for i in range(10):
        assert limiter.esta_bloqueado(f"chave-{i}") is False

    assert limiter._tentativas == {}


def test_esta_bloqueado_remove_chave_apos_janela_expirar():
    limiter = LoginRateLimiter(max_tentativas=1, janela_segundos=1)
    limiter.registrar_tentativa("vitor")
    assert "vitor" in limiter._tentativas

    time.sleep(1.1)
    limiter.esta_bloqueado("vitor")

    assert "vitor" not in limiter._tentativas
