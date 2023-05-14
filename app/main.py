from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from json.decoder import JSONDecodeError
import sched
import time
import uvicorn
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SUPER_TOKEN = os.getenv("MASTER_TOKEN")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET methods


# @app.get("/api/v1/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0,  limit: int = 100,  db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.get("/api/v1/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('Token')
    if token is None:
        raise HTTPException(
            status_code=406, detail="No Token provided.")
    elif token != SUPER_TOKEN:
        raise HTTPException(
            status_code=403, detail="Token missmatch")
    else:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.get("/api/v1/get_cur_temp/{user_id}")
async def read_cur_temp(user_id: int, request: Request, db: Session = Depends(get_db)):
    password = request.headers.get('Token')
    if password is None:
        raise HTTPException(
            status_code=406, detail="No Token provided.")    
    else:
        cur_temp = crud.get_current_temperature(db, user_id=user_id, password=password)
        return cur_temp

# PATCH, POST methods


@app.patch("/api/v1/update_cur_temp/{user_id}")
async def update_cur_temperature_for_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get('Content-Type')
    password = request.headers.get('Token')

    if password is None:
        raise HTTPException(
            status_code=406, detail="No Token provided.")
    if content_type is None:
        raise HTTPException(
            status_code=406, detail="No Content-Type provided.")
    elif content_type == 'application/json':
        try:
            json = await request.json()
            return crud.update_current_temperature(db=db, data=json, user_id=user_id, password=password)
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON data.")
    else:
        raise HTTPException(
            status_code=415, detail="Content-Type not supported.")


@app.post("/api/v1/create_user/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('Token')
    if token is None:
        raise HTTPException(
            status_code=406, detail="No Token provided.")
    elif token != SUPER_TOKEN:
        raise HTTPException(
            status_code=403, detail="Token missmatch")
    else:
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=400, detail="User with this username already exist")
        return crud.create_user(db=db, user=user)
