# backend/app/api/routes/user_stories.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user_story import UserStory

router = APIRouter()

@router.get("/{story_id}")
def get_user_story(story_id: int, db: Session = Depends(get_db)):
    """Récupérer une user story"""
    story = db.query(UserStory).filter(UserStory.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="User story not found")
    return story