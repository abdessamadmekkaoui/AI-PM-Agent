from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, date
from app.core.database import get_db
from app.models.project import Project
from app.models.task import Task
from app.models.user_story import UserStory
from app.schemas.project import ProjectCreate
from app.agents.coordinator import AgentCoordinator
from app.agents.tech_advisor_agent import TechAdvisorAgent
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate")
async def generate_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Endpoint principal qui orchestre les 3 agents pour créer un projet complet
    """
    logger.info(f"🚀 Création du projet: {project_data.name}")
    
    try:
        # Initialiser le coordinateur
        coordinator = AgentCoordinator()
        
        # Convertir les données Pydantic en dict
        project_dict = {
            "name": project_data.name,
            "description": project_data.description,
            "start_date": project_data.start_date.isoformat() if isinstance(project_data.start_date, date) else project_data.start_date
        }
        
        # Orchestrer les agents
        result = coordinator.create_project(project_dict)
        
        # Obtenir les recommandations tech
        tech_advisor = TechAdvisorAgent()
        tech_recommendations = tech_advisor.recommend_stack(project_data.description)
        
        # Créer le projet en base
        db_project = Project(
            name=result["name"],
            description=result["description"],
            start_date=datetime.fromisoformat(result["start_date"]).date(),
            status="active"
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Sauvegarder les tâches
        tasks_list = []
        for task_data in result.get("tasks", []):
            db_task = Task(
                project_id=db_project.id,
                title=task_data.get("title", ""),
                description=task_data.get("description", ""),
                duration_days=task_data.get("duration_days", 1),
                start_date=datetime.fromisoformat(task_data["start_date"]).date() if task_data.get("start_date") else None,
                end_date=datetime.fromisoformat(task_data["end_date"]).date() if task_data.get("end_date") else None,
                priority=task_data.get("priority", "medium"),
                status=task_data.get("status", "todo"),
                dependencies=task_data.get("dependencies", ""),
                order=task_data.get("order", 0)
            )
            db.add(db_task)
            tasks_list.append(db_task)
        
        # Sauvegarder les user stories
        stories_list = []
        for story_data in result.get("user_stories", []):
            db_story = UserStory(
                project_id=db_project.id,
                title=story_data.get("title", ""),
                description=story_data.get("description", ""),
                points=story_data.get("points", 0),
                priority=story_data.get("priority", "Should Have"),
                status=story_data.get("status", "todo"),
                sprint=story_data.get("sprint", 0),
                acceptance_criteria=story_data.get("acceptance_criteria", "")
            )
            db.add(db_story)
            stories_list.append(db_story)
        
        db.commit()
        
        # Rafraîchir pour obtenir les IDs
        for task in tasks_list:
            db.refresh(task)
        for story in stories_list:
            db.refresh(story)
        
        # Générer le code Mermaid pour le Gantt
        gantt_code = generate_gantt_code(result.get("tasks", []), result["name"])
        
        # Retourner la réponse complète
        return {
            "success": True,
            "project": {
                "id": db_project.id,
                "name": db_project.name,
                "description": db_project.description,
                "start_date": db_project.start_date.isoformat(),
                "created_at": db_project.created_at.isoformat() if db_project.created_at else None,
                "status": db_project.status
            },
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "duration_days": task.duration_days,
                    "start_date": task.start_date.isoformat() if task.start_date else None,
                    "end_date": task.end_date.isoformat() if task.end_date else None,
                    "priority": task.priority,
                    "status": task.status,
                    "dependencies": task.dependencies,
                    "order": task.order
                }
                for task in tasks_list
            ],
            "user_stories": [
                {
                    "id": story.id,
                    "title": story.title,
                    "description": story.description,
                    "points": story.points,
                    "priority": story.priority,
                    "status": story.status,
                    "sprint": story.sprint,
                    "acceptance_criteria": story.acceptance_criteria
                }
                for story in stories_list
            ],
            "gantt_code": gantt_code,
            "tech_recommendations": tech_recommendations,
            "metrics": result.get("metrics", {}),
            "agents_used": result.get("agents_used", [])
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.patch("/tasks/{task_id}/status")
async def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """
    Met à jour le statut d'une tâche
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    db.commit()
    db.refresh(task)
    
    return {"success": True, "task": task}


def generate_gantt_code(tasks: list, project_name: str) -> str:
    """Génère le code Mermaid pour le diagramme de Gantt"""
    gantt_lines = [
        "gantt",
        f"    title {project_name}",
        "    dateFormat YYYY-MM-DD",
        ""
    ]
    
    for task in tasks:
        status = "done" if task.get("status") == "done" else "active" if task.get("status") == "in_progress" else "crit"
        start = task.get("start_date", "")
        duration = task.get("duration_days", 1)
        
        gantt_lines.append(f"    {task.get('title', 'Task')} :{status}, {start}, {duration}d")
    
    return "\n".join(gantt_lines)


@router.patch("/tasks/{task_id}/status")
async def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    """
    Met à jour le statut d'une tâche
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if status not in ['todo', 'in_progress', 'done']:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    task.status = status
    db.commit()
    db.refresh(task)
    
    return {
        "success": True,
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status
        }
    }
