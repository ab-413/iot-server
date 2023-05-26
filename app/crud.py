from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException
from . import models, schemas, logger
from .hashing import Hasher
from .main import MASTER_TOKEN


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_chat_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).offset(skip).limit(limit).all()


def add_default_data(db: Session, id: int):
    user_data = models.CurrentData(
        data={}, owner_id=id, datetime=func.now())
    try:
        db.add(user_data)
    except:
        db.rollback()
        logger.log.error("Adding default data for user_id: %s error", user_data.owner_id)
        raise HTTPException(status_code=500, detail="Adding default data error")
    else:
        db.commit()
        db.refresh(user_data)
        logger.log.info("Adding default data for user_id: %s successful", user_data.owner_id)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password, telegram_id=user.telegram_id)
    try:
        db.add(db_user)
    except:
        db.rollback()
        logger.log.error("ERROR Adding user with username: %s id: %s", db_user.username, db_user.id)
        raise HTTPException(status_code=500, detail="Adding user error")
    else:
        db.commit()
        db.refresh(db_user)
        logger.log.info("Adding user with username: %s id: %s  telegrem_id: %s successful", db_user.username, db_user.id, db_user.telegram_id)
        add_default_data(db, db_user.id)
        return db_user


def get_current_data(db: Session, user_id: int, password: str):
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()

    if not user:
        raise HTTPException(
            status_code=404, detail="User not found")
    if Hasher.verify_password(password, user.hashed_password) or password == MASTER_TOKEN:
        return db.query(models.CurrentData).filter(models.CurrentData.owner_id == user_id).all()
    else:
        raise HTTPException(
            status_code=403, detail="Password missmatch")
    


def update_current_data(db: Session, data: schemas.CurTemp, user_id: int, password: str):
    user_data = db.query(models.CurrentData).filter(
        models.CurrentData.owner_id == user_id).one_or_none()
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    archive_data = models.ArchiveData(data=data, owner_id=user_id, datetime=func.now())

    if not user:
        raise HTTPException(
            status_code=404, detail="User not found")
    if not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=403, detail="Password missmatch")

    if not user_data:
        raise HTTPException(
            status_code=404, detail="Current data for user not found")
    try:
        user_data.data = data
        db.add(user_data)
        db.add(archive_data)
    except:
        db.rollback()
        logger.log.error("Update data error")
    else:
        db.commit()
        db.refresh(user_data)
        db.refresh(archive_data)
        return user_data
