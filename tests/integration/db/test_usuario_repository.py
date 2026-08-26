import uuid

from app.domain.entities.usuario import Usuario
from app.infrastructure.db.repositories.usuario_repository import (
    SqlAlchemyUsuarioRepository,
)


def test_add_e_get_by_login(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)
    usuario = Usuario(id=uuid.uuid4(), login="vitor", senha_hash="hash-x")

    repo.add(usuario)
    encontrado = repo.get_by_login("vitor")

    assert encontrado is not None
    assert encontrado.id == usuario.id
    assert encontrado.login == "vitor"


def test_get_by_login_retorna_none_se_nao_existir(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)

    assert repo.get_by_login("nao-existe") is None


def test_existe_algum_usuario_retorna_false_quando_vazio(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)

    assert repo.existe_algum_usuario() is False


def test_existe_algum_usuario_retorna_true_apos_add(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)
    repo.add(Usuario(id=uuid.uuid4(), login="vitor", senha_hash="hash-x"))

    assert repo.existe_algum_usuario() is True
