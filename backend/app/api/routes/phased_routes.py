# app/api/routes/phased_routes.py
"""
Nouvelles routes pour la génération phasée
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, date
from app.core.database import get_db
from app.models.project import Project
from app.models.task import Task
from app.models.user_story import UserStory
from app.schemas.project import ProjectCreate
from app.agents.planner_agent import PlannerAgent
from app.agents.scheduler_agent import SchedulerAgent
from app.agents.backlog_agent import BacklogAgent
from app.agents.tech_advisor_agent import TechAdvisorAgent
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate-tasks")
async def generate_tasks_only(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Phase 1: Génère uniquement les tâches et les recommandations tech
    """
    logger.info(f"🚀 Phase 1: Génération des tâches pour: {project_data.name}")
    
    try:
        # Créer le projet en base
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            start_date=project_data.start_date,
            status="active"
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Générer les tâches avec le Planner Agent
        planner = PlannerAgent()
        tasks_data = planner.generate_tasks(project_data.description)
        
        # Obtenir les recommandations tech
        tech_advisor = TechAdvisorAgent()
        tech_recommendations = tech_advisor.recommend_stack(project_data.description)
        
        # Sauvegarder les tâches
        tasks_list = []
        for task_data in tasks_data:
            db_task = Task(
                project_id=db_project.id,
                title=task_data.get("title", ""),
                description=task_data.get("description", ""),
                duration_days=task_data.get("duration_days", 1),
                priority=task_data.get("priority", "medium"),
                status="todo",
                dependencies=task_data.get("dependencies", ""),
                order=task_data.get("order", 0)
            )
            db.add(db_task)
            tasks_list.append(db_task)
        
        db.commit()
        
        # Rafraîchir pour obtenir les IDs
        for task in tasks_list:
            db.refresh(task)
        
        return {
            "success": True,
            "phase": "tasks_generated",
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
                    "priority": task.priority,
                    "status": task.status,
                    "dependencies": task.dependencies,
                    "order": task.order
                }
                for task in tasks_list
            ],
            "tech_recommendations": tech_recommendations,
            "message": f"✅ {len(tasks_list)} tâches générées avec succès!"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur génération tâches: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/{project_id}/generate-gantt")
async def generate_gantt(project_id: int, db: Session = Depends(get_db)):
    """
    Phase 2: Génère le diagramme Gantt pour un projet existant
    """
    logger.info(f"📅 Phase 2: Génération Gantt pour projet {project_id}")
    
    try:
        # Récupérer le projet et ses tâches
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        tasks = db.query(Task).filter(Task.project_id == project_id).order_by(Task.order).all()
        if not tasks:
            raise HTTPException(status_code=400, detail="Aucune tâche à planifier")
        
        # Utiliser le Scheduler Agent
        scheduler = SchedulerAgent()
        tasks_data = [
            {
                "id": t.id,
                "title": t.title,
                "duration_days": t.duration_days,
                "dependencies": t.dependencies,
                "priority": t.priority,
                "status": t.status
            }
            for t in tasks
        ]
        
        scheduled_tasks = scheduler.create_schedule(tasks_data, project.start_date)
        
        # Mettre à jour les dates dans la DB
        for scheduled in scheduled_tasks:
            task = db.query(Task).filter(Task.id == scheduled["id"]).first()
            if task:
                task.start_date = datetime.fromisoformat(scheduled["start_date"]).date()
                task.end_date = datetime.fromisoformat(scheduled["end_date"]).date()
        
        db.commit()
        
        # Générer le code Gantt
        gantt_code = generate_gantt_code(scheduled_tasks, project.name)
        
        return {
            "success": True,
            "phase": "gantt_generated",
            "gantt_code": gantt_code,
            "tasks": scheduled_tasks,
            "message": "✅ Diagramme Gantt généré avec succès!"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur génération Gantt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/{project_id}/generate-backlog")
async def generate_backlog(project_id: int, db: Session = Depends(get_db)):
    """
    Phase 3: Génère les user stories pour un projet existant
    """
    logger.info(f"📝 Phase 3: Génération Backlog pour projet {project_id}")
    
    try:
        # Récupérer le projet
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        # Utiliser le Backlog Agent
        backlog_agent = BacklogAgent()
        user_stories_data = backlog_agent.generate_user_stories(project.description)
        
        # Sauvegarder les user stories
        stories_list = []
        for story_data in user_stories_data:
            db_story = UserStory(
                project_id=project.id,
                title=story_data.get("title", ""),
                description=story_data.get("description", ""),
                points=story_data.get("points", 0),
                priority=story_data.get("priority", "Should Have"),
                status="todo",
                sprint=story_data.get("sprint", 0),
                acceptance_criteria=story_data.get("acceptance_criteria", "")
            )
            db.add(db_story)
            stories_list.append(db_story)
        
        db.commit()
        
        # Rafraîchir
        for story in stories_list:
            db.refresh(story)
        
        return {
            "success": True,
            "phase": "backlog_generated",
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
            "message": f"✅ {len(stories_list)} user stories générées avec succès!"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur génération Backlog: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


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
