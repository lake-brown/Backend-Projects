from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.post("/", response_model=schemas.AnswerResponse)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    user = db.query(models.User).filter(models.User.id == answer.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_answer = models.Answer(
        content=answer.content,
        question_id=answer.question_id,
        user_id=answer.user_id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

@router.get("/question/{question_id}", response_model=list[schemas.AnswerResponse])
def get_answers_by_question(question_id: int, db: Session = Depends(get_db)):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
