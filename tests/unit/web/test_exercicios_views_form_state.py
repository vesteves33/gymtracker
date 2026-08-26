import uuid

from app.domain.entities.exercicio import TipoExercicio
from app.infrastructure.web.routes.exercicios_views import ExercicioFormState


def test_form_state_sem_id_para_criacao():
    estado = ExercicioFormState(nome="Supino", tipo=TipoExercicio.MUSCULACAO)
    assert estado.id is None
    assert estado.nome == "Supino"
    assert estado.tipo is TipoExercicio.MUSCULACAO


def test_form_state_com_id_para_edicao():
    exercicio_id = uuid.uuid4()
    estado = ExercicioFormState(nome="Supino", tipo=TipoExercicio.MUSCULACAO, id=exercicio_id)
    assert estado.id == exercicio_id
