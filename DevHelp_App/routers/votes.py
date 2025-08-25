from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/{question_id}")
def vote(question_id: int, vote: schemas.VoteRequest, user_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    # For simplicity, we just return vote info
    return {"question_id": question_id, "user_id": user_id, "vote_type": vote.vote_type}
