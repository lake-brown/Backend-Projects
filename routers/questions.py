from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/", response_model=list[schemas.QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()

@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.post("/", response_model=schemas.QuestionResponse)
def create_question(q: schemas.QuestionCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == q.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_q = models.Question(title=q.title, content=q.content, user_id=q.user_id)
    db.add(new_q)
    db.commit()
    db.refresh(new_q)
    return new_q
