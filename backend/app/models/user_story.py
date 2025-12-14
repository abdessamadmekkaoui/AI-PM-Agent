from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserStory(Base):
    __tablename__ = "user_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    points = Column(Integer, default=0)
    priority = Column(String(50), default="Should Have")  # Must Have, Should Have, Could Have
    status = Column(String(50), default="todo")  # todo, in_progress, done
    sprint = Column(Integer, default=0)
    acceptance_criteria = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation
    project = relationship("Project", back_populates="user_stories")
