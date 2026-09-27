from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import router


settings = get_settings()


app = FastAPI(
    title="LegalEase API",
    description=(
        "AI-Powered Legal Document "
        "Generator API"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        settings.frontend_url,
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "application": "LegalEase",
        "status": "running",
        "documentation": "/docs",
        "health": "/health",
    }