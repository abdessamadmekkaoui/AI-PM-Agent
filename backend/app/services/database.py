from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_pm_agent.db")

# Créer le moteur de base de données
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Modèle pour les projets
class ProjectDB(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    tasks = relationship("TaskDB", back_populates="project", cascade="all, delete-orphan")
    user_stories = relationship("UserStoryDB", back_populates="project", cascade="all, delete-orphan")

# Modèle pour les tâches
class TaskDB(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, default=1)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(50), default="todo")  # todo, in_progress, done
    priority = Column(String(50), default="medium")  # low, medium, high
    dependencies = Column(Text)  # IDs des tâches dépendantes séparés par des virgules
    order = Column(Integer, default=0)
    
    # Relation
    project = relationship("ProjectDB", back_populates="tasks")

# Modèle pour les User Stories
class UserStoryDB(Base):
    __tablename__ = "user_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    points = Column(Integer, default=1)  # Story points
    priority = Column(String(50), default="Should Have")  # Must Have, Should Have, Could Have
    status = Column(String(50), default="todo")  # todo, in_progress, done
    sprint = Column(Integer, default=0)
    acceptance_criteria = Column(Text)
    
    # Relation
    project = relationship("ProjectDB", back_populates="user_stories")

# Fonction pour initialiser la base de données
def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"📦 Base de données créée: {DATABASE_URL}")

# Fonction pour obtenir une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
