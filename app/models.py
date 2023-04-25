from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    cur_temperature = relationship(
        "CurrentTemperature", back_populates="owner")


class CurrentTemperature(Base):
    __tablename__ = "cur_temperature"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"))
    datetime = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="cur_temperature")
