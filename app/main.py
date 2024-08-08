from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from .database import engine
from . import models
from .routers import admin, user
from fastapi.security import HTTPBasic, HTTPBasicCredentials

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiz API",
    description="An API for managing quizzes",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "admin",
            "description": "Admin operations"
        },
        {
            "name": "user",
            "description": "User operations"
        }
    ],
    openapi_security=[{"basicAuth": []}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, tags=["admin"])
app.include_router(user.router, tags=["user"])

# security = HTTPBasic()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Quiz API"}

# @app.post("/login")
# def login(credentials: HTTPBasicCredentials = Depends(security)):
#     return {"username": credentials.username}
