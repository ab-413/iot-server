from typing import Any
from pydantic import BaseModel, Json


class CurTempBase(BaseModel):
    pass


class CurTemp(CurTempBase):
    id: int
    owner_id: int
    data: Json[Any]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
