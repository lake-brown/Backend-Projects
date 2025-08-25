from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/", response_model=list[schemas.QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()


@router.post("/", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, user_id: int, db: Session = Depends(get_db)):
    new_question = models.Question(
        title=question.title,
        content=question.content,
        owner_id=user_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
