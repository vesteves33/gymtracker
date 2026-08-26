from fastapi import FastAPI

from app.infrastructure.web.routes.auth import router as auth_router
from app.infrastructure.web.routes.exercicios import router as exercicios_router
from app.infrastructure.web.routes.exercicios_views import router as exercicios_views_router
from app.infrastructure.web.routes.home_views import router as home_views_router

app = FastAPI(title="GymTracker")
app.include_router(home_views_router)
app.include_router(auth_router)
app.include_router(exercicios_router)
app.include_router(exercicios_views_router)
