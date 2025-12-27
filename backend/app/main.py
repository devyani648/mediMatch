from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers.search import router as search_router
from .services.embedding_service import get_embedding_service


app = FastAPI(title="MediMatch")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    # Load embedding service on startup
    get_embedding_service(device=settings.device)


@app.get("/")
def root():
    return {"message": "Welcome to MediMatch"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(search_router)
