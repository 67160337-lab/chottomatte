from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine

from backend.routes.auth_routes import router as auth_router
from backend.routes.water_routes import router as water_router
from backend.routes.aerator_routes import router as aerator_router
from backend.routes.ai_routes import router as ai_router


# =========================
# Create Database
# =========================

Base.metadata.create_all(
    bind=engine
)


# =========================
# FastAPI
# =========================

app = FastAPI(
    title="Wastewater AI API",
    description=(
        "REST API for wastewater "
        "quality monitoring and "
        "AI aerator prediction"
    ),
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================
# Routes
# =========================

app.include_router(
    auth_router
)

app.include_router(
    water_router
)

app.include_router(
    aerator_router
)

app.include_router(
    ai_router
)


# =========================
# Root
# =========================

@app.get("/")
def root():

    return {
        "message": "Wastewater AI API is running",
        "docs": "/docs"
    }
