import os
import uuid

os.environ.setdefault("JWT_SECRET", "test-secret")

from app.infrastructure.auth.jwt import JwtTokenGenerator  # noqa: E402


def test_generate_e_decode_roundtrip():
    generator = JwtTokenGenerator()
    usuario_id = uuid.uuid4()

    token = generator.generate(usuario_id)
    decoded_id = JwtTokenGenerator.decode(token)

    assert decoded_id == usuario_id
