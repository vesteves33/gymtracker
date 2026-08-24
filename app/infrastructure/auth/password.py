import bcrypt

from app.domain.ports.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, senha: str) -> str:
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, senha: str, senha_hash: str) -> bool:
        try:
            return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
        except ValueError:
            return False
