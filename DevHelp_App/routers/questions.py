from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(tags=["Questions"])


# Get all questions
@router.get("/", response_model=list[schemas.QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()


# Get a single question by ID
@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question



# Create a question
@router.post("/", response_model=schemas.QuestionResponse)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db)
):
    # Validate that the user exists
    user = db.query(models.User).filter(models.User.id == question.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_question = models.Question(
        title=question.title,
        content=question.content,
        user_id=question.user_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question
