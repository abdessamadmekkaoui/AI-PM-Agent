from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration_days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    priority = Column(String(50), default="medium")  # low, medium, high
    status = Column(String(50), default="todo")  # todo, in_progress, done
    dependencies = Column(Text, nullable=True)  # Comma-separated task IDs
    order = Column(Integer, default=0)
    
    # Relations
    project = relationship("Project", back_populates="tasks")
