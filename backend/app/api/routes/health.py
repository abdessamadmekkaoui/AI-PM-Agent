from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI PM Agent API",
        "version": "1.0.0"
    }
