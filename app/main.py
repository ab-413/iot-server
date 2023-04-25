from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from json.decoder import JSONDecodeError
import sched
import time
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET methods


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/get_cur_temp/{user_id}")
def read_cur_temp(user_id: int, db: Session = Depends(get_db)):
    cur_temp = crud.get_current_temperature(db, user_id=user_id)
    return cur_temp

# PATCH, POST methods


@app.patch("/update_cur_temp/{user_id}")
async def update_cur_temperature_for_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get('Content-Type')

    if content_type is None:
        raise HTTPException(
            status_code=406, detail="No Content-Type provided.")
    elif content_type == 'application/json':
        try:
            json = await request.json()
            return crud.update_current_temperature(db=db, data=json, user_id=user_id)
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON data.")
    else:
        raise HTTPException(
            status_code=415, detail="Content-Type not supported.")


@app.post("/create_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="User with this username already exist")
    return crud.create_user(db=db, user=user)


def do_something(scheduler):
    # schedule the next call first
    scheduler.enter(60, 1, do_something, (scheduler,))
    print("Doing stuff...")
    # then do your stuff


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, do_something, (my_scheduler,))

if __name__ == "__main__":
    my_scheduler.run()
    uvicorn.run(app, host='0.0.0.0', port=8000,
                reload=True, debug=True, workers=3)
