import secrets

from fastapi import HTTPException, Response

CSRF_COOKIE_NAME = "csrf_token"


def ensure_csrf_cookie(response: Response, csrf_token: str | None) -> str:
    """Retorna o token existente ou gera+seta um novo cookie CSRF."""
    if csrf_token:
        return csrf_token
    token = secrets.token_urlsafe(32)
    response.set_cookie(CSRF_COOKIE_NAME, token, httponly=True, samesite="strict")
    return token


def copy_set_cookie_headers(source: Response, target: Response) -> None:
    """Copia headers Set-Cookie de `source` para `target`.

    Necessario porque `ensure_csrf_cookie` recebe um `Response` provisorio para
    poder gerar o token antes de renderizar o template (o token precisa estar
    disponivel no contexto do Jinja2 antes da resposta final ser construida).
    O FastAPI so mescla headers de uma dependencia `Response` injetada quando a
    rota retorna um valor nao-Response; como as views retornam `TemplateResponse`
    diretamente, o cookie provisorio precisa ser copiado manualmente.
    """
    target.raw_headers.extend(h for h in source.raw_headers if h[0] == b"set-cookie")


def verify_csrf_token(csrf_token_cookie: str | None, csrf_token_form: str | None) -> None:
    if (
        not csrf_token_cookie
        or not csrf_token_form
        or not secrets.compare_digest(csrf_token_cookie.encode(), csrf_token_form.encode())
    ):
        raise HTTPException(status_code=403, detail="CSRF invalido")
