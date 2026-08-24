import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.domain.ports.token_generator import TokenGenerator

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60 * 24


class JwtTokenGenerator(TokenGenerator):
    def generate(self, usuario_id: uuid.UUID) -> str:
        secret = os.environ["JWT_SECRET"]
        payload = {
            "sub": str(usuario_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES),
        }
        return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode(token: str) -> uuid.UUID:
        secret = os.environ["JWT_SECRET"]
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return uuid.UUID(payload["sub"])
