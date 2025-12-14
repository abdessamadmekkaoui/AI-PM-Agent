# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import projects, agent_routes, phased_routes
from app.models import project, task, user_story  # Import all models

# Créer les tables
Base.metadata.create_all(bind=engine)

# Initialiser FastAPI
app = FastAPI(
    title="AI PM Agent API",
    description="API pour le système multi-agents de gestion de projets",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(phased_routes.router, prefix="/api/projects", tags=["phased"])
app.include_router(agent_routes.router, prefix="/api/projects", tags=["agents"])
app.include_router(projects.router, prefix="/api", tags=["projects"])

@app.get("/")
async def root():
    return {
        "message": "AI PM Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)