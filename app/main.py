from fastapi import FastAPI

from app.infrastructure.logging_config import configure_logging
from app.infrastructure.web.current_user import UsuarioNaoAutenticadoView
from app.infrastructure.web.routes.auth import router as auth_router
from app.infrastructure.web.routes.exercicios import router as exercicios_router
from app.infrastructure.web.routes.exercicios_views import router as exercicios_views_router

configure_logging()

app = FastAPI(title="GymTracker")
app.include_router(auth_router)
app.include_router(exercicios_router)
app.include_router(exercicios_views_router)
