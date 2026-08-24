from app.infrastructure.auth.password import BcryptPasswordHasher


def test_hash_e_verify_roundtrip():
    hasher = BcryptPasswordHasher()

    hash_gerado = hasher.hash("minhasenha123")

    assert hash_gerado != "minhasenha123"
    assert hasher.verify("minhasenha123", hash_gerado) is True


def test_verify_falha_com_senha_errada():
    hasher = BcryptPasswordHasher()
    hash_gerado = hasher.hash("minhasenha123")

    assert hasher.verify("senha-errada", hash_gerado) is False


def test_verify_com_senha_maior_que_72_bytes_retorna_false_sem_crashar():
    hasher = BcryptPasswordHasher()
    hash_gerado = hasher.hash("minhasenha123")

    assert hasher.verify("x" * 100, hash_gerado) is False
