from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def createQuestion(db: Session, quiz: schemas.QuizCreate):
    try:
        db_quiz = models.Quiz(admin_username=quiz.admin_username, question=quiz.question, answer=quiz.answer)
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create quiz: {e}")

def getQuizController(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Quiz).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve quizzes: {e}")

def getQuestion(db: Session):
    try:
        quizzes = db.query(models.Quiz.id, models.Quiz.question).all()
        return [{"id": quiz.id, "question": quiz.question} for quiz in quizzes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve quiz questions: {e}")

def editQuiz(db: Session, quiz_id: int, quiz: schemas.QuizUpdate):
    try:
        db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
        if db_quiz:
            db_quiz.question = quiz.question
            db_quiz.answer = quiz.answer
            db.commit()
            db.refresh(db_quiz)
        return db_quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update quiz: {e}")

def removeQuiz(db: Session, quiz_id: int):
    try:
        db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
        if db_quiz:
            db.delete(db_quiz)
            db.commit()
        return db_quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete quiz: {e}")

def CreateUser(db: Session, user: schemas.UserCreate):
    try:
        db_user = models.User(username=user.username, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {e}")

def getUser(db: Session, username: str):
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {e}")

def submitAnswer(db: Session, username: str, question_id: int, answer: str):
    try:
        user = get_user_by_username(db, username=username)
        if not user:
            return None
        if user.submit_count >= 10:
            return "Limit Over"

        quiz = db.query(models.Quiz).filter(models.Quiz.id == question_id).first()
        if not quiz or quiz.answer != answer:
            return None

        user.submit_count += 1
        user.score += quiz.marks
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {e}")

def getScore(db: Session, username: str):
    try:
        user = get_user_by_username(db, username=username)
        return user.score if user else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user score: {e}")
