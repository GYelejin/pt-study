from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey

from .base import BaseModel


class UsersTable(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(True), server_default=func.now())

    username = Column(String(64), unique=True, index=True)
