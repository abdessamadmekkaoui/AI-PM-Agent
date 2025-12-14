from app.services.gemini_service import gemini_service
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PlannerAgent:
    def __init__(self):
        self.name = "Planner Agent"
        self.description = "Génère les tâches détaillées du projet"
    
    def generate_tasks(self, project_description: str) -> List[Dict[str, Any]]:
        """
        Génère 15-20 tâches détaillées pour un projet
        """
        logger.info("🤖 Planner Agent: Génération des tâches...")
        
        try:
            tasks = gemini_service.generate_tasks(project_description)
            
            logger.info(f"✅ Planner Agent: {len(tasks)} tâches générées")
            return tasks
            
        except Exception as e:
            logger.error(f"❌ Planner Agent error: {e}")
            # Retourner des tâches par défaut
            return gemini_service._get_default_tasks()
