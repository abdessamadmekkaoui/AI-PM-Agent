from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SchedulerAgent:
    def __init__(self):
        self.name = "Scheduler Agent"
        self.description = "Crée le planning et le diagramme de Gantt"
    
    def create_schedule(self, tasks: List[Dict[str, Any]], start_date: datetime) -> List[Dict[str, Any]]:
        """
        Calcule les dates de début et fin pour chaque tâche
        """
        logger.info("📅 Scheduler Agent: Création du planning...")
        
        # Trier les tâches par ordre et dépendances
        scheduled_tasks = []
        
        # Dictionnaire pour stocker les dates de fin par tâche
        end_dates = {}
        
        for task in tasks:
            task_id = str(task["id"])
            duration = task.get("duration_days", 1)
            
            # Calculer la date de début
            if "dependencies" in task and task["dependencies"]:
                # Dépend de la fin de la dernière tâche dépendante
                deps = str(task["dependencies"]).split(",")
                latest_end = start_date
                
                for dep_id in deps:
                    dep_id = dep_id.strip()
                    if dep_id in end_dates:
                        dep_end = end_dates[dep_id]
                        if dep_end > latest_end:
                            latest_end = dep_end
                
                task_start = latest_end
            else:
                # Pas de dépendances, commence à la date de début du projet
                task_start = start_date
            
            # Calculer la date de fin
            task_end = task_start + timedelta(days=duration)
            
            # Mettre à jour end_dates
            end_dates[task_id] = task_end
            
            # Ajouter les dates à la tâche
            scheduled_task = task.copy()
            scheduled_task["start_date"] = task_start.isoformat()
            scheduled_task["end_date"] = task_end.isoformat()
            
            scheduled_tasks.append(scheduled_task)
        
        # Trier par date de début
        scheduled_tasks.sort(key=lambda x: x["start_date"])
        
        logger.info(f"✅ Scheduler Agent: Planning créé pour {len(scheduled_tasks)} tâches")
        return scheduled_tasks
    
    def calculate_project_duration(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcule la durée totale du projet
        """
        if not tasks:
            return {"total_days": 0, "end_date": None}
        
        # Trouver la date de fin la plus tardive
        end_dates = [datetime.fromisoformat(task["end_date"]) for task in tasks if task.get("end_date")]
        
        if not end_dates:
            return {"total_days": 0, "end_date": None}
        
        max_end_date = max(end_dates)
        
        # Calculer la durée totale
        start_dates = [datetime.fromisoformat(task["start_date"]) for task in tasks if task.get("start_date")]
        min_start_date = min(start_dates) if start_dates else datetime.now()
        
        total_days = (max_end_date - min_start_date).days + 1
        
        return {
            "total_days": total_days,
            "start_date": min_start_date.isoformat(),
            "end_date": max_end_date.isoformat()
        }
