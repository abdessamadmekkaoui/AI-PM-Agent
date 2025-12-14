from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List

# Schéma de base
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date

# Schéma pour la création
class ProjectCreate(ProjectBase):
    pass

# Schéma pour la mise à jour
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    status: Optional[str] = None

# Schéma de réponse
class Project(ProjectBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)