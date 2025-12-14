from app.services.gemini_service import gemini_service
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BacklogAgent:
    def __init__(self):
        self.name = "Backlog Agent"
        self.description = "Génère les User Stories et le backlog Agile"
    
    def generate_user_stories(self, project_description: str) -> List[Dict[str, Any]]:
        """
        Génère 10-15 User Stories pour le projet
        """
        logger.info("📝 Backlog Agent: Génération des User Stories...")
        
        try:
            stories = gemini_service.generate_user_stories(project_description)
            
            # Assigner les stories aux sprints (simplifié)
            for i, story in enumerate(stories):
                story["sprint"] = (i // 5) + 1  # 5 stories par sprint
            
            logger.info(f"✅ Backlog Agent: {len(stories)} User Stories générées")
            return stories
            
        except Exception as e:
            logger.error(f"❌ Backlog Agent error: {e}")
            return gemini_service._get_default_stories()
    
    def calculate_velocity(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcule la vélocité estimée du projet
        """
        total_points = sum(story.get("points", 0) for story in stories)
        
        # Estimation simplifiée
        sprints_needed = max(1, total_points // 20)  # 20 points par sprint
        
        return {
            "total_points": total_points,
            "sprints_needed": sprints_needed,
            "velocity_estimate": 20,
            "must_have_points": sum(s.get("points", 0) for s in stories if s.get("priority") == "Must Have"),
            "should_have_points": sum(s.get("points", 0) for s in stories if s.get("priority") == "Should Have"),
            "could_have_points": sum(s.get("points", 0) for s in stories if s.get("priority") == "Could Have")
        }
