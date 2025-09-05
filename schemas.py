from pydantic import BaseModel, EmailStr
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

UserOut = UserResponse

# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# Question schemas
class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    user_id: int

class QuestionResponse(QuestionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Answer schemas
class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    question_id: int
    user_id: int

class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Vote schemas
class VoteRequest(BaseModel):
    vote_type: str

class VoteResponse(BaseModel):
    question_id: int
    user_id: int
    vote_type: str

    class Config:
        from_attributes = True
