import time
from collections import defaultdict


class LoginRateLimiter:
    def __init__(self, max_tentativas: int = 5, janela_segundos: int = 300) -> None:
        self._max_tentativas = max_tentativas
        self._janela_segundos = janela_segundos
        self._tentativas: dict[str, list[float]] = defaultdict(list)

    def registrar_tentativa(self, chave: str) -> None:
        self._tentativas[chave].append(time.monotonic())

    def esta_bloqueado(self, chave: str) -> bool:
        agora = time.monotonic()
        limite = agora - self._janela_segundos
        tentativas = [t for t in self._tentativas[chave] if t > limite]
        self._tentativas[chave] = tentativas
        return len(tentativas) >= self._max_tentativas
