import uuid

from app.domain.entities.exercicio import Exercicio, TipoExercicio


def test_cria_exercicio_musculacao():
    exercicio_id = uuid.uuid4()
    exercicio = Exercicio(id=exercicio_id, nome="Supino", tipo=TipoExercicio.MUSCULACAO)

    assert exercicio.id == exercicio_id
    assert exercicio.nome == "Supino"
    assert exercicio.tipo == TipoExercicio.MUSCULACAO


def test_tipo_exercicio_tem_valores_esperados():
    assert TipoExercicio.MUSCULACAO.value == "musculacao"
    assert TipoExercicio.AEROBICO.value == "aerobico"
