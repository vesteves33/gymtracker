MIN_JWT_SECRET_LENGTH = 32
FORBIDDEN_SECRETS = {"changeme"}


def validate_jwt_secret(secret: str | None) -> None:
    if not secret:
        raise RuntimeError("JWT_SECRET nao definido")
    if secret in FORBIDDEN_SECRETS:
        raise RuntimeError("JWT_SECRET nao pode usar o valor padrao 'changeme'")
    if len(secret) < MIN_JWT_SECRET_LENGTH:
        raise RuntimeError(f"JWT_SECRET deve ter pelo menos {MIN_JWT_SECRET_LENGTH} caracteres")
