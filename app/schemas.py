from pydantic import BaseModel

class QuizCreate(BaseModel):
    admin_username: str
    question: str
    answer: str

class QuizUpdate(BaseModel):
    question: str
    answer: str

class UserCreate(BaseModel):
    username: str
    password: str

class AnswerSubmit(BaseModel):
    username: str
    question_id: int
    answer: str
