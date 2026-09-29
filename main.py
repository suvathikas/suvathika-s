from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router


app = FastAPI(
    title="LegalEase API",
    description=(
        "AI-assisted legal document drafting "
        "demonstration. Not legal advice."
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to LegalEase",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "LegalEase API is running"
    }