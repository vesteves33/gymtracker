import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.infrastructure.auth.secret_check import validate_jwt_secret
from app.infrastructure.web.current_user import UsuarioNaoAutenticadoView
from app.infrastructure.web.routes.auth import router as auth_router
from app.infrastructure.web.routes.exercicios import router as exercicios_router
from app.infrastructure.web.routes.exercicios_views import router as exercicios_views_router
from app.infrastructure.web.routes.home_views import router as home_views_router

validate_jwt_secret(os.environ.get("JWT_SECRET"))

app = FastAPI(title="GymTracker")


@app.exception_handler(UsuarioNaoAutenticadoView)
def redirecionar_para_login(request: Request, exc: UsuarioNaoAutenticadoView) -> RedirectResponse:
    return RedirectResponse(url="/", status_code=303)


app.include_router(home_views_router)
app.include_router(auth_router)
app.include_router(exercicios_router)
app.include_router(exercicios_views_router)
