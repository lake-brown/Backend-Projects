from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.post("/", response_model=schemas.AnswerResponse)
def create_answer(answer: schemas.AnswerCreate, user_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    new_answer = models.Answer(
        content=answer.content,
        question_id=answer.question_id,
        owner_id=user_id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

@router.get("/{answer_id}", response_model=schemas.AnswerResponse)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@router.get("/question/{question_id}", response_model=list[schemas.AnswerResponse])
def get_answers_by_question(question_id: int, db: Session = Depends(get_db)):
    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    return answers
