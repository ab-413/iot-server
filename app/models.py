from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    telegram_id = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    current_data = relationship(
        "CurrentData", back_populates="owner")


class CurrentData(Base):
    __tablename__ = "current_data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"))
    datetime = Column(DateTime(timezone=True))

    owner = relationship("User", back_populates="current_data")


class ArchiveData(Base):
    __tablename__ = "archive_data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    owner_id = Column(Integer, ForeignKey("users.id"))
    datetime = Column(DateTime(timezone=True))
