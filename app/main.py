from fastapi import FastAPI

from app.infrastructure.web.routes.auth import router as auth_router

app = FastAPI(title="GymTracker")
app.include_router(auth_router)
