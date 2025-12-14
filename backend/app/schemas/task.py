from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_days: int
    priority: str = "medium"
    dependencies: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    dependencies: Optional[str] = None

class Task(TaskBase):
    id: int
    project_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    order: int
    
    class Config:
        from_attributes = True
