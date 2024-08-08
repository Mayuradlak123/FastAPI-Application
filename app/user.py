from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import get_db

router = APIRouter()

@router.post("/user/create_user", response_model=schemas.UserCreate, summary="Create a new user")
def CreateUser(
    username: str = Query(..., description="Username for the new user"), 
    password: str = Query(..., description="Password for the new user"), 
    db: Session = Depends(get_db)
):
    """
    Create a new user with the given username and password.
    """
    try:
        db_user = crud.get_user_by_username(db, username=username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        user = schemas.UserCreate(username=username, password=password)
        return crud.create_user(db, user=user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/user/take_test", summary="Take a test")
def AttemptTest(
    username: str = Query(..., description="Username of the user taking the test"), 
    db: Session = Depends(get_db)
):
    """
    Allow a user to take a test by retrieving quiz questions.
    """
    try:
        user = crud.get_user_by_username(db, username=username)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        return crud.get_quiz_only_question(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/user/submit_answer", summary="Submit an answer")
def SubmitTest(
    username: str = Query(..., description="Username of the user submitting the answer"), 
    question_id: int = Query(..., description="ID of the question being answered"), 
    answer: str = Query(..., description="Answer to the question"), 
    db: Session = Depends(get_db)
):
    """
    Submit an answer for a given question.
    """
    try:
        result = crud.submit_answer(db, username=username, question_id=question_id, answer=answer)
        if result == "Limit Over":
            raise HTTPException(status_code=400, detail="Submission limit is over")
        if not result:
            raise HTTPException(status_code=400, detail="Answer submission failed or user not found")
        return {"message": "Answer submitted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/user/score", summary="Get user score")
def getScore(
    username: str = Query(..., description="Username of the user"), 
    db: Session = Depends(get_db)
):
    """
    Get the score of a user.
    """
    try:
        score = crud.get_user_score(db, username=username)
        if score is None:
            raise HTTPException(status_code=400, detail="User not found")
        return {"username": username, "score": score}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
