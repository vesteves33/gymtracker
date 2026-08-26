import pytest
from fastapi import HTTPException, Response

from app.infrastructure.web.csrf import copy_set_cookie_headers, verify_csrf_token


def test_verify_aceita_tokens_iguais():
    verify_csrf_token(csrf_token_cookie="abc123", csrf_token_form="abc123")


def test_verify_rejeita_tokens_diferentes():
    with pytest.raises(HTTPException) as exc_info:
        verify_csrf_token(csrf_token_cookie="abc123", csrf_token_form="outro")
    assert exc_info.value.status_code == 403


def test_verify_rejeita_cookie_ausente():
    with pytest.raises(HTTPException) as exc_info:
        verify_csrf_token(csrf_token_cookie=None, csrf_token_form="abc123")
    assert exc_info.value.status_code == 403


def test_verify_rejeita_token_nao_ascii_sem_lancar_type_error():
    with pytest.raises(HTTPException) as exc_info:
        verify_csrf_token(csrf_token_cookie="abc123", csrf_token_form="café")
    assert exc_info.value.status_code == 403


def test_verify_rejeita_tokens_nao_ascii_diferentes():
    with pytest.raises(HTTPException) as exc_info:
        verify_csrf_token(csrf_token_cookie="café", csrf_token_form="cafè")
    assert exc_info.value.status_code == 403


def test_copy_set_cookie_headers_copia_apenas_set_cookie():
    source = Response()
    source.set_cookie("csrf_token", "abc123")
    target = Response()

    copy_set_cookie_headers(source, target)

    cookie_headers = [h for h in target.raw_headers if h[0] == b"set-cookie"]
    assert len(cookie_headers) == 1
    assert b"csrf_token=abc123" in cookie_headers[0][1]


def test_copy_set_cookie_headers_nao_copia_content_length():
    source = Response()
    target = Response()
    headers_antes = list(target.raw_headers)

    copy_set_cookie_headers(source, target)

    assert target.raw_headers == headers_antes
