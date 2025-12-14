# backend/app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task

router = APIRouter()

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Récupérer une tâche"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """Mettre à jour le statut d'une tâche"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    db.commit()
    db.refresh(task)
    return task