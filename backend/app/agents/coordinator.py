from app.agents.planner_agent import PlannerAgent
from app.agents.scheduler_agent import SchedulerAgent
from app.agents.backlog_agent import BacklogAgent
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AgentCoordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.scheduler = SchedulerAgent()
        self.backlog = BacklogAgent()
    
    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestre les 3 agents pour créer un projet complet
        """
        logger.info("🚀 Agent Coordinator: Démarrage de la création de projet...")
        
        try:
            # Étape 1: Planner Agent - Générer les tâches
            logger.info("Étape 1/3: Génération des tâches...")
            tasks = self.planner.generate_tasks(project_data["description"])
            
            # Étape 2: Scheduler Agent - Créer le planning
            logger.info("Étape 2/3: Création du planning...")
            start_date = datetime.fromisoformat(project_data["start_date"]) if isinstance(project_data["start_date"], str) else project_data["start_date"]
            scheduled_tasks = self.scheduler.create_schedule(tasks, start_date)
            
            # Étape 3: Backlog Agent - Générer les User Stories
            logger.info("Étape 3/3: Génération du backlog...")
            user_stories = self.backlog.generate_user_stories(project_data["description"])
            
            # Calculer les métriques
            project_duration = self.scheduler.calculate_project_duration(scheduled_tasks)
            velocity = self.backlog.calculate_velocity(user_stories)
            
            # Créer le projet complet
            project = {
                "name": project_data["name"],
                "description": project_data["description"],
                "start_date": start_date.isoformat(),
                "created_at": datetime.utcnow().isoformat(),
                "tasks": scheduled_tasks,
                "user_stories": user_stories,
                "metrics": {
                    "project_duration": project_duration,
                    "agile_metrics": velocity
                },
                "agents_used": [
                    {"name": self.planner.name, "status": "completed"},
                    {"name": self.scheduler.name, "status": "completed"},
                    {"name": self.backlog.name, "status": "completed"}
                ]
            }
            
            logger.info("✅ Agent Coordinator: Projet créé avec succès!")
            return project
            
        except Exception as e:
            logger.error(f"❌ Agent Coordinator error: {e}")
            raise Exception(f"Erreur lors de la création du projet: {str(e)}")
