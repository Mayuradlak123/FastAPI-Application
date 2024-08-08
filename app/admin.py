from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db

router = APIRouter()

# Hardcoded admin credentials
username = "admin"
psw = "12345"

security = HTTPBasic()

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == username and credentials.password == psw:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

@router.post("/admin/create-question", response_model=schemas.QuizCreate, summary="Create a new question")
def createQuestion(
    question: str, 
    answer: str, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    """
    Create a new quiz question.
    """
    try:
        quiz = schemas.QuizCreate(admin_username=username, question=question, answer=answer)
        return crud.create_quiz(db, quiz=quiz)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/admin/get-questions", summary="Get list of questions")
def readQuestion(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    """
    Retrieve a list of quiz questions.
    """
    try:
        return crud.get_quiz(db, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.put("/admin/update-question/{quiz_id}", summary="Update an existing question")
def updateQuestion(
    quiz_id: int,
    question: str,
    answer: str,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    """
    Update a quiz question by its ID.
    """
    try:
        quiz = schemas.QuizUpdate(question=question, answer=answer)
        return crud.update_quiz(db, quiz_id=quiz_id, quiz=quiz)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.delete("/admin/delete-question/{quiz_id}", summary="Delete a question")
def deleteQuestion(
    quiz_id: int, 
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin)
):
    """
    Delete a quiz question by its ID.
    """
    try:
        return crud.delete_quiz(db, quiz_id=quiz_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
