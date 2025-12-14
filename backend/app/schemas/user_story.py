from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Schéma de base
class UserStoryBase(BaseModel):
    title: str
    user_type: Optional[str] = None
    action: Optional[str] = None
    benefit: Optional[str] = None
    story_points: Optional[int] = None
    priority: Optional[str] = None
    sprint_number: Optional[int] = None

# Schéma pour la création
class UserStoryCreate(UserStoryBase):
    project_id: int

# Schéma pour la mise à jour
class UserStoryUpdate(BaseModel):
    title: Optional[str] = None
    user_type: Optional[str] = None
    action: Optional[str] = None
    benefit: Optional[str] = None
    story_points: Optional[int] = None
    priority: Optional[str] = None
    sprint_number: Optional[int] = None

# Schéma de réponse
class UserStory(UserStoryBase):
    id: int
    project_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)