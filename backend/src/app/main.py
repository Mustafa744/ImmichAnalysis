from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router

app = FastAPI(
    title="Immich Analysis API",
    description="Backend API for advanced photo analysis, clustering, and intelligent search.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Immich Analysis API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
